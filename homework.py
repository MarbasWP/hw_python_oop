from dataclasses import dataclass, asdict, fields
from typing import Collection


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO = ('Тип тренировки: {training_type}; ' 
            'Длительность: {duration:.3f} ч.; ' 
            'Дистанция: {distance:.3f} км; ' 
            'Ср. скорость: {speed:.3f} км/ч; ' 
            'Потрачено ккал: {calories:.3f}.'
            )

    def get_message(self) -> str:
        return self.INFO.format(**asdict(self))


@dataclass()
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM = 1000
    HOUR_IN_MIN = 60
    LEN_STEP = 0.65

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
    SPEED_MULTIPLIER_1 = 18
    SPEED_SHIFT = 20

    def get_spent_calories(self):
        return (
            (
                self.SPEED_MULTIPLIER_1
                * self.get_mean_speed()
                - self.SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.HOUR_IN_MIN
        )


@dataclass()
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029
    COEFFICIENT_DEGREE = 2

    def get_spent_calories(self) -> float:
        return (
            (
                self.WEIGHT_MULTIPLIER_1
                * self.weight
                +
                (
                        self.get_mean_speed()
                        ** self.COEFFICIENT_DEGREE
                        // self.height
                )
                * self.WEIGHT_MULTIPLIER_2
                * self.weight
            )
            * self.duration
            * self.HOUR_IN_MIN
        )


@dataclass()
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    SWIMMING_SPEED_SHIFT = 1.1
    SPEED_MULTIPLIER_2 = 2

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
                )

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.SWIMMING_SPEED_SHIFT)
                * self.SPEED_MULTIPLIER_2 * self.weight
                )


SPORTS = {
    'RUN': (Running, len(fields(Running))),
    'WLK': (SportsWalking, len(fields(SportsWalking))),
    'SWM': (Swimming, len(fields(Swimming)))
}

ERROR_SPORT = '{} нет в базе данных.'
ERROR_PARAMETERS = 'Для {} необходимо {} параметра, а вы ввели {}.'


def read_package(workout: str, date: Collection) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout not in SPORTS:
        raise ValueError(ERROR_SPORT.format(workout))
    sport, parameters = (SPORTS.get(workout)[0],
                         SPORTS.get(workout)[1]
                         )
    if parameters != len(date):
        raise ValueError(
            ERROR_PARAMETERS.format
                        (
                            workout,
                            parameters,
                            len(date)
                        )
        )
    return sport(*date)


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
        main(read_package(workout_type, data))
