import abc



class EnemyDeathObserver():
    @abc.abstractmethod
    def notificar(self):
        pass

