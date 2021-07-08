# by Esmail :)
import tkinter
from .app import clock, attendance, init
from typing import Dict, Union, Callable, TypeVar, Generic, List
T = TypeVar("T")


class Console:
    def __init__(self):
        self.data: List[str] = []

    def write(self, data: str):
        self.data.append(data)


class Queue(Generic[T]):
    def __init__(self):
        self.arr: List[T] = []

    def dequeue(self) -> T:
        if self.arr:
            return self.arr.pop()

    def enqueue(self, data: T):
        self.arr.insert(0, data)

    def front(self) -> T:
        if self.arr:
            return self.arr[-1]


class Intersection:
    def __init__(self, intersection_id: str):
        self.id = intersection_id
        self.north_south: bool = True  # Green
        self.east_west: bool = False  # Red
        self.agent: Union[None, str] = None  # No one is here

    def change_light(self, side: int, color: int, console: Console):
        if side == 0 and color == 0 and self.east_west:
            console.write(f"Both sides are Green at {self.id}.")
        elif side == 1 and color == 0 and self.north_south:
            console.write(f"Both sides are Green at {self.id}.")
        if side == 0:
            self.north_south = not color
            console.write(f"{self.id}: North-South changed to "
                          f"{'Red' if color else 'Green'}.")
        elif side == 1:
            self.east_west = not color
            console.write(f"{self.id}: East-West changed to "
                          f"{'Red' if color else 'Green'}.")

    def set_agent(self, agent_id: str):
        self.agent = agent_id


class AgentNode:
    def __init__(self, agent_id: str, intersection_id: str, time: int):
        self.id = agent_id
        self.intersection = intersection_id
        self.time = time + 600


class Simulator:
    def __init__(self,
                 after_callback: Callable,
                 console: Console,
                 clock_callback: Callable,
                 attendance_callback: Callable
                 ):
        self.clock_callback = clock_callback
        self.attendance_callback = attendance_callback
        self.console = console
        self.intersections: Dict[str, Intersection] = {}
        self.sleep_timer = 990  # millisecond
        self.after_callback = after_callback
        self.agents_queue: Queue[AgentNode] = Queue()
        self.time = 0

    def light(self, intersection_id: str, side: int, color: int):
        assert 0 <= side < 2
        assert 0 <= color < 2
        if intersection_id not in self.intersections:
            self.intersections[intersection_id] = Intersection(intersection_id)
        self.intersections[intersection_id].change_light(side, color,
                                                         self.console)

    def sms(self, agent_id: str, intersection_id: str):
        ag = AgentNode(agent_id, intersection_id, self.time)
        self.console.write(f"Agent {agent_id} got SMS for {intersection_id}")
        self.agents_queue.enqueue(ag)

    def mainloop(self):
        #  here is the Event loop
        while True:
            ag = self.agents_queue.front()
            if ag and ag.time == self.time:
                self.agents_queue.dequeue()
                self.attendance_callback(ag.intersection, ag.id)
                self.console.write(f"Agent {ag.id} attended"
                                   f" at {ag.intersection}.")
            else:
                break
        # Traffic Data Process :(
        self.time += 1
        self.after_callback(self.sleep_timer, self.mainloop)


class Panel(tkinter.Tk):
    pass


if __name__ == '__main__':
    pass
