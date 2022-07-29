from dataclasses import dataclass, asdict
from typing import Collection


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO = ('Тип тренировки: {}; '
            'Длительность: {:.3f} ч.; '
            'Дистанция: {:.3f} км; '
            'Ср. скорость: {:.3f} км/ч; '
            'Потрачено ккал: {:.3f}.'
            )

    def get_message(self) -> str:
        return self.INFO.format(*asdict(self).values())


@dataclass()
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM = 1000
    HOUR_IN_MIN = 60
    LEN_STEP = 0.65
    SPEED_MULTIPLIER_2 = 2

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
        return ((self.SPEED_MULTIPLIER_1
                 * self.get_mean_speed()
                 - self.SPEED_SHIFT)
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

    def get_spent_calories(self) -> float:
        return ((self.WEIGHT_MULTIPLIER_1
                 * self.weight
                 + (self.get_mean_speed()
                    ** self.SPEED_MULTIPLIER_2
                    // self.height)
                 * self.WEIGHT_MULTIPLIER_2
                 * self.weight)
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
    'RUN': (Running, len(Running.__dataclass_fields__)),
    'WLK': (SportsWalking, len(SportsWalking.__dataclass_fields__)),
    'SWM': (Swimming, len(Swimming.__dataclass_fields__))
}

ERROR_SPORT = '{} нет в базе данных.'
ERROR_PARAMETERS = 'Для {} необходимо {} параметра, а вы ввели {}.'


def read_package(workout_type: str, date: Collection) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in SPORTS:
        raise ValueError(ERROR_SPORT.format(workout_type))
    elif SPORTS.get(workout_type)[1] != len(date):
        raise ValueError(ERROR_PARAMETERS.format(workout_type,
                                                 SPORTS.get(workout_type)[1],
                                                 len(date)
                                                 )
                         )
    return SPORTS.get(workout_type)[0](*date)


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