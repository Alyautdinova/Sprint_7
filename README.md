# Sprint_7

## API-тесты

Проект содержит API-тесты для сервиса «Яндекс.Самокат», написанные на Python + Pytest + Requests + Allure.

### Что проверяется

- **Создание курьера**
- **Логин курьера**
- **Создание заказа**
- **Получение списка заказов**

### Запуск тестов с Allure

```bash
# 1. Запустить тесты с сохранением результатов
pytest --alluredir=target/allure-results --clean-alluredir

# 2. Сгенерировать HTML-отчёт
allure generate target/allure-results -o target/allure-report --clean

# 3. Открыть отчёт локально
allure open target/allure-report
```
