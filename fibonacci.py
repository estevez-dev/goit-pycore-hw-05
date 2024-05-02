def caching_fibonacci():
    # Створюємо кеш обчислень
    cache = {}

    # Сама функція обчислення, або діставання з кешу
    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        elif n in cache:
            return cache[n] # Повернення кешованого значення

        # Рекурсія! І кешування нового значення
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        
        # Повернення кешованого значення
        return cache[n]

    # Повернення функції обчислення
    return fibonacci