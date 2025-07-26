#!/usr/bin/env python3

import yaml
import sys
import time
import signal
import shlex
import os
import threading
import logging
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import importlib.util
import subprocess


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'

def colored_print(text, color, prefix=""):
    print(f"{color}{prefix}{text}{Colors.RESET}")

def print_header(title):
    print("\n" + "="*60)
    colored_print(f" {title} ", Colors.BOLD + Colors.CYAN)
    print("="*60)

@dataclass
class ServiceConfig:
    name: str
    command: List[str] = field(default_factory=list)
    working_dir: Optional[str] = None
    env: Dict[str, str] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    startup_delay: int = 0
    color: str = "white"
    enabled: bool = True
    python_function: Optional[str] = None
    module_path: Optional[str] = None
    post_start_hook: Optional[str] = None

@dataclass
class ComposerConfig:
    services: Dict[str, ServiceConfig] = field(default_factory=dict)
    global_env: Dict[str, str] = field(default_factory=dict)
    startup_order: List[str] = field(default_factory=list)
    hooks: Dict[str, List[str]] = field(default_factory=dict)

class ServiceComposer:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config: Optional[ComposerConfig] = None
        self.threads: List[threading.Thread] = []
        self.running = True
        self.services_status: Dict[str, str] = {}  # "starting", "running", "stopped", "error"
        self.service_outputs: Dict[str, List[str]] = {}
        self.color_map = {
            "red": Colors.RED,
            "green": Colors.GREEN,
            "yellow": Colors.YELLOW,
            "blue": Colors.BLUE,
            "magenta": Colors.MAGENTA,
            "cyan": Colors.CYAN,
            "white": Colors.RESET
        }

        # Настройка логирования
        self.setup_logging()

        # Установка обработчика сигналов
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger(__name__)

    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        colored_print("\n🛑 Получен сигнал завершения. Останавливаем сервисы...", Colors.YELLOW)
        self.stop_all()
        sys.exit(0)

    def load_config(self, config_path: str) -> bool:
        """Загрузка конфигурации из YAML файла"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            self.config = ComposerConfig()

            # Загрузка глобальных переменных окружения
            self.config.global_env = data.get('global_env', {})

            # Загрузка порядка запуска
            self.config.startup_order = data.get('startup_order', [])

            # Загрузка хуков
            self.config.hooks = data.get('hooks', {})

            # Загрузка сервисов
            services_data = data.get('services', {})
            for service_name, service_config in services_data.items():
                # Обработка команды - может быть строкой или списком
                command = service_config.get('command', [])
                if isinstance(command, str):
                    # Разбиваем строку на части для shell команд
                    command = shlex.split(command)

                service = ServiceConfig(
                    name=service_name,
                    command=command,
                    working_dir=service_config.get('working_dir'),
                    env=service_config.get('env', {}),
                    depends_on=service_config.get('depends_on', []),
                    startup_delay=service_config.get('startup_delay', 0),
                    color=service_config.get('color', 'white'),
                    enabled=service_config.get('enabled', True),
                    python_function=service_config.get('python_function'),
                    module_path=service_config.get('module_path'),
                    post_start_hook=service_config.get('post_start_hook')
                )
                self.config.services[service_name] = service
                self.services_status[service_name] = "stopped"
                self.service_outputs[service_name] = []

            colored_print(f"✅ Конфигурация загружена из {config_path}", Colors.GREEN)
            return True

        except FileNotFoundError:
            colored_print(f"❌ Файл конфигурации не найден: {config_path}", Colors.RED)
            return False
        except yaml.YAMLError as e:
            colored_print(f"❌ Ошибка парсинга YAML: {e}", Colors.RED)
            return False
        except Exception as e:
            colored_print(f"❌ Ошибка загрузки конфигурации: {e}", Colors.RED)
            return False

    def create_example_config(self, output_path: str = "service-composer.yaml"):
        """Создание примера конфигурации"""
        example_config = {
            'global_env': {
                'PYTHONPATH': '.',
                'ENVIRONMENT': 'development'
            },
            'startup_order': ['backend', 'frontend', 'telegram_bot'],
            'hooks': {
                'pre_start': ['echo "Запуск сервисов..."'],
                'post_start': ['echo "Все сервисы запущены!"']
            },
            'services': {
                'backend': {
                    'command': ['python', '-m', 'uvicorn', 'src.main:app', '--host', '0.0.0.0', '--port', '8000', '--reload'],
                    'working_dir': 'backend',
                    'color': 'green',
                    'startup_delay': 2,
                    'env': {
                        'PORT': '8000'
                    },
                    'enabled': True
                },
                'frontend': {
                    'command': ['python', 'server.py'],
                    'working_dir': 'frontend',
                    'color': 'blue',
                    'startup_delay': 1,
                    'depends_on': ['backend'],
                    'enabled': True
                },
                'telegram_bot': {
                    'command': ['python', 'main.py'],
                    'working_dir': 'tg_bot',
                    'color': 'magenta',
                    'startup_delay': 3,
                    'depends_on': ['backend'],
                    'enabled': True
                },
                'ngrok': {
                    'command': ['ngrok', 'start', '--config', 'ngrok.yml', '--all'],
                    'working_dir': '.',
                    'color': 'cyan',
                    'startup_delay': 0,
                    'enabled': False
                },
                'custom_function': {
                    'python_function': 'custom_startup_function',
                    'module_path': 'custom_module.py',
                    'color': 'yellow',
                    'startup_delay': 0,
                    'enabled': False
                }
            }
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(example_config, f, default_flow_style=False, allow_unicode=True, indent=2)
            colored_print(f"✅ Пример конфигурации создан: {output_path}", Colors.GREEN)
            return True
        except Exception as e:
            colored_print(f"❌ Ошибка создания конфигурации: {e}", Colors.RED)
            return False

    def run_hooks(self, hook_type: str):
        """Выполнение хуков"""
        if not self.config or hook_type not in self.config.hooks:
            return

        hooks = self.config.hooks[hook_type]
        colored_print(f"🪝 Выполнение {hook_type} хуков...", Colors.YELLOW)

        for hook in hooks:
            try:
                result = subprocess.run(hook, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    colored_print(f"✅ Хук выполнен: {hook}", Colors.GREEN)
                    if result.stdout:
                        print(result.stdout.strip())
                else:
                    colored_print(f"❌ Ошибка хука: {hook}", Colors.RED)
                    if result.stderr:
                        print(result.stderr.strip())
            except Exception as e:
                colored_print(f"❌ Ошибка выполнения хука {hook}: {e}", Colors.RED)

    def run_service_hook(self, hook_name: str, service_name: str):
        """Выполнение хука сервиса"""
        if not self.config or hook_name not in self.config.hooks:
            colored_print(f"⚠️ Хук {hook_name} не найден для сервиса {service_name}", Colors.YELLOW)
            return

        hooks = self.config.hooks[hook_name]
        colored_print(f"🪝 Выполнение хука {hook_name} для {service_name}...", Colors.YELLOW)

        for hook in hooks:
            try:
                result = subprocess.run(hook, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    colored_print(f"✅ Хук выполнен: {hook}", Colors.GREEN)
                    if result.stdout:
                        print(result.stdout.strip())
                else:
                    colored_print(f"❌ Ошибка хука: {hook}", Colors.RED)
                    if result.stderr:
                        print(result.stderr.strip())
            except Exception as e:
                colored_print(f"❌ Ошибка выполнения хука {hook}: {e}", Colors.RED)

    def call_python_function(self, service: ServiceConfig):
        """Вызов Python функции вместо команды"""
        if not service.python_function or not service.module_path:
            colored_print(f"❌ Неполная конфигурация Python функции для {service.name}", Colors.RED)
            return

        try:
            # Загрузка модуля
            spec = importlib.util.spec_from_file_location("custom_module", service.module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Получение функции
            function = getattr(module, service.python_function)

            # Вызов функции
            colored_print(f"🐍 Вызов Python функции: {service.python_function}",
                          self.color_map.get(service.color, Colors.RESET), f"[{service.name}] ")

            result = function()

            colored_print(f"✅ Функция {service.python_function} выполнена",
                          self.color_map.get(service.color, Colors.RESET), f"[{service.name}] ")

            if result:
                colored_print(str(result),
                              self.color_map.get(service.color, Colors.RESET), f"[{service.name}] ")

        except Exception as e:
            colored_print(f"❌ Ошибка вызова функции {service.python_function}: {e}", Colors.RED)
            self.services_status[service.name] = "error"

    def run_service(self, service: ServiceConfig):
        """Запуск отдельного сервиса"""
        if not service.enabled:
            colored_print(f"⏭️ Сервис {service.name} отключен", Colors.YELLOW)
            return

        self.services_status[service.name] = "starting"
        color = self.color_map.get(service.color, Colors.RESET)

        # Задержка перед запуском
        if service.startup_delay > 0:
            colored_print(f"⏳ Ожидание {service.startup_delay} сек перед запуском {service.name}...",
                          Colors.YELLOW)
            time.sleep(service.startup_delay)

        try:
            # Если это Python функция
            if service.python_function:
                self.call_python_function(service)
                return

            # Если это обычная команда
            if not service.command:
                colored_print(f"❌ Команда не указана для сервиса {service.name}", Colors.RED)
                self.services_status[service.name] = "error"
                return

            colored_print(f"🚀 Запуск {service.name}...", color, f"[{service.name}] ")
            colored_print(f"Команда: {' '.join(service.command)}", Colors.BLUE, f"[{service.name}] ")

            # Подготовка окружения
            env = os.environ.copy()
            env.update(self.config.global_env)
            env.update(service.env)

            # Запуск процесса
            proc = subprocess.Popen(
                service.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=service.working_dir,
                env=env,
                bufsize=1,
                universal_newlines=False
            )

            self.services_status[service.name] = "running"

            # Выполнение хука после запуска сервиса
            if service.post_start_hook:
                self.run_service_hook(service.post_start_hook, service.name)

            # Чтение вывода в реальном времени
            while self.running and proc.poll() is None:
                try:
                    line = proc.stdout.readline()
                    if line:
                        line = line.decode('utf-8', errors='ignore').rstrip()
                        if line:  # Не печатаем пустые строки
                            colored_print(line, color, f"[{service.name}] ")
                            self.service_outputs[service.name].append(line)
                except:
                    break

            # Проверка кода завершения
            if proc.returncode != 0 and self.running:
                colored_print(f"❌ Сервис {service.name} завершился с ошибкой (код: {proc.returncode})",
                              Colors.RED)
                self.services_status[service.name] = "error"
            else:
                self.services_status[service.name] = "stopped"

        except Exception as e:
            colored_print(f"❌ Ошибка запуска {service.name}: {e}", Colors.RED)
            self.services_status[service.name] = "error"

    def check_dependencies(self, service_name: str) -> bool:
        """Проверка зависимостей сервиса"""
        if not self.config or service_name not in self.config.services:
            return False

        service = self.config.services[service_name]
        for dep in service.depends_on:
            if dep not in self.services_status:
                colored_print(f"❌ Зависимость {dep} не найдена для {service_name}", Colors.RED)
                return False
            if self.services_status[dep] != "running":
                colored_print(f"⏳ Ожидание запуска зависимости {dep} для {service_name}...",
                              Colors.YELLOW)
                return False

        return True

    def get_startup_order(self) -> List[str]:
        """Получение порядка запуска сервисов"""
        if not self.config:
            return []

        # Если задан явный порядок
        if self.config.startup_order:
            # Добавляем сервисы, не указанные в startup_order
            explicit_order = [s for s in self.config.startup_order if s in self.config.services]
            remaining = [s for s in self.config.services.keys() if s not in explicit_order]
            return explicit_order + remaining

        # Автоматический порядок на основе зависимостей
        ordered = []
        remaining = list(self.config.services.keys())

        while remaining:
            # Находим сервисы без неразрешенных зависимостей
            ready = []
            for service_name in remaining:
                service = self.config.services[service_name]
                if all(dep in ordered for dep in service.depends_on):
                    ready.append(service_name)

            if not ready:
                # Циклическая зависимость или ошибка
                colored_print("❌ Обнаружена циклическая зависимость или ошибка в конфигурации",
                              Colors.RED)
                ordered.extend(remaining)
                break

            # Добавляем готовые сервисы
            for service_name in ready:
                ordered.append(service_name)
                remaining.remove(service_name)

        return ordered

    def run_all_services(self):
        """Запуск всех сервисов согласно конфигурации"""
        if not self.config:
            colored_print("❌ Конфигурация не загружена", Colors.RED)
            return False

        print_header("🚀 Запуск сервисов")

        # Выполнение хуков перед запуском
        self.run_hooks('pre_start')

        # Получение порядка запуска
        startup_order = self.get_startup_order()
        enabled_services = [s for s in startup_order if self.config.services[s].enabled]

        colored_print(f"📋 Порядок запуска: {' → '.join(enabled_services)}", Colors.CYAN)

        # Запуск сервисов
        for service_name in startup_order:
            if not self.config.services[service_name].enabled:
                continue

            service = self.config.services[service_name]

            # Ожидание зависимостей
            max_wait = 30  # максимальное время ожидания зависимостей
            wait_time = 0
            while not self.check_dependencies(service_name) and wait_time < max_wait:
                time.sleep(1)
                wait_time += 1

            if wait_time >= max_wait:
                colored_print(f"❌ Превышено время ожидания зависимостей для {service_name}",
                              Colors.RED)
                continue

            # Запуск сервиса в отдельном потоке
            thread = threading.Thread(
                target=self.run_service,
                args=(service,),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)

            # Небольшая задержка между запусками
            time.sleep(0.5)

        # Выполнение хуков после запуска
        time.sleep(2)  # Даем время сервисам запуститься
        self.run_hooks('post_start')

        colored_print("✅ Все сервисы запущены!", Colors.GREEN)
        colored_print("📝 Логи отображаются ниже. Нажмите Ctrl+C для остановки.", Colors.YELLOW)
        print("="*60 + "\n")

        try:
            # Ожидание завершения
            while self.running:
                # Проверяем статус сервисов
                running_count = sum(1 for status in self.services_status.values()
                                    if status in ["starting", "running"])
                if running_count == 0:
                    colored_print("ℹ️ Все сервисы завершились", Colors.YELLOW)
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()

        return True

    def stop_all(self):
        """Остановка всех сервисов"""
        self.running = False
        colored_print("🧹 Останавливаем все сервисы...", Colors.YELLOW)

        # Выполнение хуков перед остановкой
        self.run_hooks('pre_stop')

        # Ожидание завершения потоков
        for thread in self.threads:
            thread.join(timeout=1)

        # Выполнение хуков после остановки
        self.run_hooks('post_stop')

        # Обновление статусов
        for service_name in self.services_status:
            if self.services_status[service_name] in ["starting", "running"]:
                self.services_status[service_name] = "stopped"

    def show_status(self):
        """Показать статус сервисов"""
        if not self.config:
            colored_print("❌ Конфигурация не загружена", Colors.RED)
            return

        print_header("📊 Статус сервисов")

        for service_name, service in self.config.services.items():
            status = self.services_status[service_name]
            color = Colors.GREEN if status == "running" else Colors.RED if status == "error" else Colors.YELLOW

            enabled_text = "✅" if service.enabled else "⏸️"
            colored_print(f"{enabled_text} {service_name}: {status}", color)

    def show_menu(self):
        """Показать интерактивное меню"""
        print_header("🎛️ Service Composer")
        print("1. 🚀 Запустить все сервисы")
        print("2. 📊 Показать статус")
        print("3. 🔄 Перезагрузить конфигурацию")
        print("4. 📋 Показать конфигурацию")
        print("5. 🛑 Остановить все сервисы")
        print("0. ❌ Выход")
        print("="*60)

        try:
            choice = input("Выберите опцию (0-5): ").strip()
            return choice
        except KeyboardInterrupt:
            return "0"

    def show_config(self):
        """Показать текущую конфигурацию"""
        if not self.config:
            colored_print("❌ Конфигурация не загружена", Colors.RED)
            return

        print_header("📋 Текущая конфигурация")

        colored_print(f"📁 Конфигурация из: {self.config_path}", Colors.CYAN)
        colored_print(f"🌍 Глобальные переменные: {self.config.global_env}", Colors.BLUE)
        colored_print(f"📝 Порядок запуска: {self.config.startup_order}", Colors.GREEN)

        print("\n🔧 Сервисы:")
        for name, service in self.config.services.items():
            status_icon = "✅" if service.enabled else "⏸️"
            colored_print(f"  {status_icon} {name}:", Colors.BOLD)

            if service.command:
                colored_print(f"    📜 Команда: {' '.join(service.command)}", Colors.BLUE)
            elif service.python_function:
                colored_print(f"    🐍 Python функция: {service.python_function}", Colors.BLUE)

            if service.working_dir:
                colored_print(f"    📁 Рабочая папка: {service.working_dir}", Colors.YELLOW)
            if service.depends_on:
                colored_print(f"    🔗 Зависимости: {', '.join(service.depends_on)}", Colors.MAGENTA)
            if service.startup_delay:
                colored_print(f"    ⏱️ Задержка: {service.startup_delay} сек", Colors.CYAN)

    def run_interactive(self):
        """Интерактивный режим"""
        while True:
            choice = self.show_menu()

            if choice == "0":
                colored_print("👋 До свидания!", Colors.CYAN)
                break
            elif choice == "1":
                self.run_all_services()
            elif choice == "2":
                self.show_status()
            elif choice == "3":
                if self.config_path:
                    self.load_config(self.config_path)
                else:
                    colored_print("❌ Путь к конфигурации не указан", Colors.RED)
            elif choice == "4":
                self.show_config()
            elif choice == "5":
                self.stop_all()
            else:
                colored_print("❌ Неверный выбор, попробуйте снова", Colors.RED)

def main():
    parser = argparse.ArgumentParser(description="Service Composer - запуск нескольких команд одновременно")
    parser.add_argument('-c', '--config', help='Путь к файлу конфигурации YAML')
    parser.add_argument('--create-config', action='store_true', help='Создать пример конфигурации')
    parser.add_argument('--status', action='store_true', help='Показать статус сервисов')

    args = parser.parse_args()

    # Создание примера конфигурации
    if args.create_config:
        composer = ServiceComposer()
        composer.create_example_config()
        return

    # Инициализация composer
    composer = ServiceComposer(args.config)

    # Загрузка конфигурации
    if args.config:
        if not composer.load_config(args.config):
            sys.exit(1)
    else:
        # Поиск конфигурации в стандартных местах
        config_files = ['service-composer.yaml', 'service-composer.yml', 'composer.yaml', 'composer.yml']
        config_found = False

        for config_file in config_files:
            if Path(config_file).exists():
                colored_print(f"📁 Найдена конфигурация: {config_file}", Colors.CYAN)
                if composer.load_config(config_file):
                    composer.config_path = config_file
                    config_found = True
                    break

        if not config_found:
            colored_print("❌ Конфигурация не найдена. Создайте её с помощью --create-config", Colors.RED)
            sys.exit(1)

    # Выполнение команд
    if args.status:
        composer.show_status()
    else:
        if len(sys.argv) == 1 or (len(sys.argv) == 3 and args.config):
            # Интерактивный режим
            composer.run_interactive()
        else:
            # Прямой запуск
            composer.run_all_services()

if __name__ == "__main__":
    main() 