from abc import ABC, abstractmethod


class Notifier(ABC):
    

    @abstractmethod
    def send(self, message):
        raise NotImplementedError


class EmailNotifier(Notifier):
    

    def send(self, message):
       
        return f"SENT: {message}"