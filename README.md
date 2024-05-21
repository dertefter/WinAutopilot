# WinAutopilot
Буквально автопилот для Windows 10 / Windows 11.

### Как это работает?
Под капотом - ChatGPT.</br>
В двух словах: если бот понимает, что для выполнения задачи ему нужено что-то сделать в Windows, он это делает.</br>
Бот пишет код на Python, который выполняет действия в Windows в реальном времени.


### Примечание
ChatGPT не даёт точных ответов. Поэтому бот может не понять ваш запрос или выполнить его неправильно.</br>
Тем не менее, этот бот имеет почти полный доступ к вашей системе, поэтому будьте осторожны.</br>

### Установка и запуск
```
git clone https://github.com/dertefter/WinAutopilot.git
```
```
cd WinAutopilot
```
```
python -m venv venv
```
```
call venv\Scripts\activate.bat
```
```
pip install -r requirements.txt
```
```
python main.py
```