class ChatDto:
  def __init__(self, **kwargs) -> None:
    self.message = kwargs.get("message")
    self.language = kwargs.get("language")