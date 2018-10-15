from app.tasks import simulate_sleep, proceed_document
from app.tests.testcase import OTestCase


class QueueTaskTest(OTestCase):
    def test_sleep_main_thread(self):
        self.assertIsNone(None)
        simulate_sleep(5)

    def test_sleep_background_thread(self):
        self.assertIsNone(None)
        simulate_sleep.delay(5)

    def test_dlnn_main_thread(self):
        self.assertIsNone(None)
        proceed_document(1)

    def test_dlnn_background_thread(self):
        self.assertIsNone(None)
        proceed_document.delay(1)
