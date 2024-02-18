# Використовуємо останню версію Ubuntu як базовий образ
FROM ubuntu:latest

# Встановлюємо необхідні пакети
RUN apt-get update && apt-get install -y openssh-server sudo

# Створюємо директорію для SSH демона
RUN mkdir /var/run/sshd

# Встановлюємо пароль для користувача root
RUN echo 'root:ki41test' | chpasswd

# Додаємо користувача root до групи sudo
RUN usermod -aG sudo root

# Відкриваємо порт 22 для SSH
EXPOSE 22

# Запускаємо SSH демон
CMD ["/usr/sbin/sshd", "-D"]
