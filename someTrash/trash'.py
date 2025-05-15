import ray

# Инициализация Ray
ray.init()

# Создание удаленной функции
@ray.remote
def square(x):
    return x * x

# Запуск задач параллельно
futures = [square.remote(i) for i in range(10000)]
results = ray.get(futures)  # Получение результатов

# Вычисление суммы
total_sum = sum(results)
print("Sum of squares:", total_sum)

# Завершение работы Ray
ray.shutdown()