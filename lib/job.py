#!/usr/bin/env python

"""
job.py
Mixin for Abstract Tester

Descript how job processed detaily.
"""

import asyncio
import aiohttp
import asyncssh
import kafka
import sys
import json

class BaseJobMixin:
    job_id = None
    job = None


class CouchDBJobStorageMixin(BaseJobMixin):
    couchdb_host = "localhost"
    couchdb_port = 8080

    def get_job_query(self, job_id):
        return "http://%s:%d/log/%s" % (self.couchdb_host, self.couchdb_port, job_id)

    async def get_job(self, job_id):
        response = await aiohttp.request("GET", self.get_job_query(job_id))
        chunk = await response.content.read()
        response.close()
        return json.loads(chunk.decode('utf-8'))


class SSHJobMixin(BaseJobMixin):
    async def do_ssh_job(self, 
            host, 
            port, 
            username, 
            password, 
            cmd_list, 
            async_callback=None, *args, **kwargs):
        with await asyncssh.connect(
                host, 
                port=port, 
                username=username, 
                password=password, 
                known_hosts=None) as conn:
            for cmd in cmd_list:
                self.logger.info("$ %s" % cmd)
                stdin, stdout, stderr = await conn.open_session(cmd)
                output = await stdout.read()
                if async_callback:
                    await async_callback(output)
                status = stdout.channel.get_exit_status()
                if status:
                    self.logger.info("Script finished with %d. Stop." % status)
                    break
                else:
                    continue


class CurlJobMixin(BaseJobMixin):
    async def do_curl_job(self, url, method="GET", **kwargs):
        response = await aiohttp.request("GET", url)
        chunk = await response.content.read()
        response.close()
        return chunk.decode('utf-8')


class KafkaWriteJobMixin(BaseJobMixin):
    def do_kafka_write_job(self, *args, **kwargs):
        producer = kafka.SimpleProducer(kafka, async=True)
        producer.send_messages(b'my-topic', b'async message')
