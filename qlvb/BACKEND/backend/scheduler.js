// Scheduler - Tự động kiểm tra và gửi email nhắc nhở mỗi ngày
// Sử dụng node-cron để chạy scheduled tasks

const cron = require('node-cron');
const emailService = require('./email-service');

class Scheduler {
    constructor() {
        this.jobs = [];
        this.isRunning = false;
    }

    /**
     * Khởi động daily reminder job
     * Chạy mỗi ngày lúc 8:00 AM
     * @param {function} checkAndSendFunction - Hàm xử lý check và gửi email
     */
    startDailyReminders(checkAndSendFunction) {
        // Cron expression: '0 8 * * *' = Every day at 8:00 AM
        const job = cron.schedule('0 8 * * *', async () => {
            console.log('\n=== Running daily deadline check ===');
            console.log(new Date().toLocaleString('vi-VN'));

            try {
                await checkAndSendFunction();
                console.log('✓ Daily reminder check completed');
            } catch (error) {
                console.error('✗ Error in daily reminder:', error);
            }
        });

        this.jobs.push(job);
        this.isRunning = true;
        console.log('✓ Daily reminder scheduler started (runs at 8:00 AM every day)');
    }

    /**
     * Tạo job custom với cron expression
     * @param {string} cronExpression - Cron expression
     * @param {function} taskFunction - Hàm cần chạy
     * @param {string} jobName - Tên job (optional)
     */
    createCustomJob(cronExpression, taskFunction, jobName = 'Custom Job') {
        const job = cron.schedule(cronExpression, async () => {
            console.log(`\n=== Running ${jobName} ===`);
            console.log(new Date().toLocaleString('vi-VN'));

            try {
                await taskFunction();
                console.log(`✓ ${jobName} completed`);
            } catch (error) {
                console.error(`✗ Error in ${jobName}:`, error);
            }
        });

        this.jobs.push(job);
        console.log(`✓ ${jobName} scheduled: ${cronExpression}`);
        return job;
    }

    /**
     * Dừng tất cả scheduled jobs
     */
    stopAll() {
        this.jobs.forEach(job => job.stop());
        this.jobs = [];
        this.isRunning = false;
        console.log('✓ All scheduled jobs stopped');
    }

    /**
     * Trigger thủ công (cho testing)
     * @param {function} checkAndSendFunction - Hàm xử lý check và gửi email
     */
    async runNow(checkAndSendFunction) {
        console.log('\n=== Manual trigger: Deadline check ===');
        console.log(new Date().toLocaleString('vi-VN'));

        try {
            await checkAndSendFunction();
            console.log('✓ Manual check completed');
        } catch (error) {
            console.error('✗ Error in manual check:', error);
            throw error;
        }
    }
}

module.exports = new Scheduler();
