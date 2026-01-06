#ifndef TASK_H
#define TASK_H

#include <iostream>
#include <string>

class Task {
public:
    int id;
    std::string description;
    int priority;
    bool isDone;

    Task(int taskId, const std::string& taskDescription, int taskPriority);

    void markDone();
    bool isitDone() const;
    void display() const;
    bool operator<(const Task& other) const;
    bool operator>(const Task& other) const;
    bool operator==(const Task& other) const;
    std::string toString() const;
};

#endif // TASK_H
