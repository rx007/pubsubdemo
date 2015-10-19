from abstract import *
from lib.job import *
from lib.logging import *
from lib.queue import *
import json
import functools

class TaasWorker(
        AMQPQueueMixin,
        CouchDBJobStorageMixin,
        SSHJobMixin,
        CurlJobMixin,
        BaseLoggingMixin,
        AbstractTester
        ):
    """docstring for TaasWorker"""

    async def process_output(self, job_id, data):
        self.logger.info("job[%s] > %s" % (job_id, data))
        job = await self.get_job(job_id)
        if not "output"  in job["tasks"]:
            job["tasks"]["output"] = []
        job["tasks"]["output"].append(data)
        await self.put_job(job_id, job)

    async def do_work(self, job_id):
        """
        called For each job
        """
        self.logger.info("> Job[%s] started" % job_id)
        job = await self.get_job(job_id)
        ssh_host = job['tasks']['ssh_host']
        ssh_port = job['tasks']['ssh_port']
        ssh_username = job['tasks']['ssh_username']
        ssh_password = job['tasks']['ssh_password']
        cmd_list = job['tasks']['script']
        print(ssh_host, ssh_port, ssh_username, ssh_password)
        await self.do_ssh_job(
                ssh_host,
                ssh_port,
                ssh_username,
                ssh_password,
                cmd_list, 
                async_callback=functools.partial(self.process_output, job_id)
                )
        self.logger.info("> Job[%s] Finished" % job_id)

    async def job_callback(self, body, envelope, properties, *args, **kwargs):
        """
        Subscript to RabbmtMQ, create tasks and detach them.
        """
        job_id = json.loads(body.decode('utf-8'))['id']
        asyncio.get_event_loop().create_task(self.do_work(job_id))


def main():
    worker = TaasWorker()
    worker.run_forever()

if __name__ == '__main__':
    main()
