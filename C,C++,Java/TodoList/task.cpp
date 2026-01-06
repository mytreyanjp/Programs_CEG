#include "task.h"

Task::Task(int taskId, const std::string& taskDescription, int taskPriority)
    : id(taskId), description(taskDescription), priority(taskPriority), isDone(false) {}

void Task::markDone() {
    isDone = true;
}

bool Task::isitDone() const {
    return isDone;
}

void Task::display() const {
    std::cout << "Task ID: " << id << " - " << description << " [" << (isDone ? "Done" : "Not Done") << "] (Priority: " << priority << ")\n" << std::endl;
}

bool Task::operator<(const Task& other) const {
    return priority < other.priority;
}

bool Task::operator>(const Task& other) const {
    return priority > other.priority;
}

bool Task::operator==(const Task& other) const {
    return id == other.id;
}

std::string Task::toString() const {
    return "Task ID: " + std::to_string(id) + " - " + description + " [" + (isDone ? "Done" : "Not Done") + "] (Priority: " + std::to_string(priority) + ")";
}
