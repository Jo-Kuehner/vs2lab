import channel
import logging

from context import lab_logging

#lab_logging.setup(stream_level=logging.DEBUG)
lab_logging.setup(stream_level=logging.INFO)

client = channel.Client()
client.run()
