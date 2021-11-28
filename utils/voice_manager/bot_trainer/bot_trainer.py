from utils.voice_manager.bot_trainer.bot_intents_reader import BotIntentsReader
from utils.voice_manager.bot_trainer.bot_loader import BotLoader
from utils.voice_manager.bot_trainer.bot_model_creator import BotModelCreator


if __name__ == '__main__':
    bot_data = BotIntentsReader("intents.yml")
    bot_model = BotModelCreator(bot_data=bot_data)

    bot_model.train_model()
    bot_model.save_models()

    bot = BotLoader(bot_model)
    print(bot.chatbot_response('Привет'))
