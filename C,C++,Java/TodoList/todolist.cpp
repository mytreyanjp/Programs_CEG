#include "todolist.h"

ToDoList::ToDoList() : nextId(1) {}

Task* ToDoList::findTaskById(typename SplayTree<Task>::Node* node, int taskId) const {
    if (!node) return nullptr;
    if (node->data.id == taskId) return &(node->data);
    if (node->left) {
        Task* found = findTaskById(node->left, taskId);
        if (found) return found;
    }
    if (node->right) {
        Task* found = findTaskById(node->right, taskId);
        if (found) return found;
    }
    return nullptr;
}

void ToDoList::addTask(const std::string& description, int priority) {
    taskTree.insert(Task(nextId++, description, priority));
}

void ToDoList::removeTask(int taskId, bool forceRemove) {
    Task* task = findTaskById(taskTree.getRoot(), taskId);
    if (task) {
        if (task->isitDone() || forceRemove) {
            taskTree.remove(*task);
        }
    }
}

void ToDoList::markTaskDone(int taskId) {
    Task* task = findTaskById(taskTree.getRoot(), taskId);
    if (task) {
        task->markDone();
    }
}

std::string ToDoList::displayTasks() const {
    return taskTree.getTasksAsString();
}

Task ToDoList::getMostPrioritizedTask() const {
    Task mostPrioritizedTask(0, "", 0);
    auto currentNode = taskTree.getRoot();
    while (currentNode) {
        if (currentNode->data > mostPrioritizedTask) {
            mostPrioritizedTask = currentNode->data;
        }
        currentNode = currentNode->right;
    }
    return mostPrioritizedTask;
}
