from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apscheduler.triggers.interval import IntervalTrigger

from app.services.cleanup_service import CardCleanupService


class SchedulerManager:

    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start_scheduler(self):

        self.scheduler.add_job(
            CardCleanupService.perform_full_cleanup,
            trigger=IntervalTrigger(hours = 24),
            id='daily_card_and_transaction_cleanup',
            replace_existing=True,
            name='Daily card expiration check and cleanup, transaction cleanup'
        )

        self.scheduler.start()

    def shutdown_scheduler(self):
        if self.scheduler.running:
            self.scheduler.shutdown()

scheduler_manager = SchedulerManager()