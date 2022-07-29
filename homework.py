from dataclasses import dataclass
from typing import Collection


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    PHRASE_INFO = ('Тип тренировки: {training_type}; '
                   'Длительность: {duration:.3f} ч.; '
                   'Дистанция: {distance:.3f} км; '
                   'Ср. скорость: {speed:.3f} км/ч; '
                   'Потрачено ккал: {calories:.3f}.'
                   )

    def get_message(self) -> str:
        return self.PHRASE_INFO.format(training_type=self.training_type,
                                       duration=self.duration,
                                       distance=self.distance,
                                       speed=self.speed,
                                       calories=self.calories
                                       )


@dataclass()
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM = 1000
    HOUR_IN_MIN = 60
    LEN_STEP = 0.65
    NUMBER_2 = 2

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass()
class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER = 18
    SPEED_SHIFT = 20

    def get_spent_calories(self):
        return ((self.SPEED_MULTIPLIER * self.get_mean_speed()
                - self.SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.HOUR_IN_MIN
                )


@dataclass()
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: float
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029

    def get_spent_calories(self) -> float:
        return ((self.WEIGHT_MULTIPLIER_1 * self.weight
                + (self.get_mean_speed() * self.NUMBER_2 // self.height)
                * self.WEIGHT_MULTIPLIER_2 * self.weight)
                * self.duration * self.HOUR_IN_MIN
                )


@dataclass()
class Swimming(Training):
    """Тренировка: плавание."""
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    SWIMMING_SPEED_SHIFT = 1.1

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
                )

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.SWIMMING_SPEED_SHIFT)
                * self.NUMBER_2 * self.weight
                )


SPORTS = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming
}


def read_package(workout_type: str, data: Collection) -> Training:
    """Прочитать данные полученные от датчиков."""
    if SPORTS.get(workout_type) is None:
        raise ValueError('Неккоректный вид спорта')
    return SPORTS.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        try:
            main(read_package(workout_type, data))
        except ValueError:
            print('Неккоректный вид спорта')
        except TypeError:
            print('Неккоректно введены данные')