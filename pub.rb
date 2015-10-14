require "bunny"
require "json"


data = {
    "id"=> "2"
}
connection = Bunny.new
connection.start

channel  = connection.create_channel
queue_name = "taas.test_queue"
queue = channel.queue(queue_name, :durable => false, :auto_delete => true)

queue.publish(JSON.dump(data), :routing_key => queue.name)
connection.close
