from app import create_app

# Создаем экземпляр приложения с использованием конфигурации по умолчанию
app = create_app()

if __name__ == "__main__":
    # Запускаем приложение
    app.run(debug=True)  # Для режима разработки
