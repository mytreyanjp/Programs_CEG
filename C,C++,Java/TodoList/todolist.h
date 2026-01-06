#ifndef TODOLIST_H
#define TODOLIST_H

#include "task.h"
#include "splay_tree.h"

class ToDoList {
private:
    SplayTree<Task> taskTree;
    int nextId;

    Task* findTaskById(typename SplayTree<Task>::Node* node, int taskId) const;

public:
    ToDoList();
    void addTask(const std::string& description, int priority);
    void removeTask(int taskId, bool forceRemove);
    void markTaskDone(int taskId);
    std::string displayTasks() const;
    Task getMostPrioritizedTask() const;
};

#endif // TODOLIST_H
