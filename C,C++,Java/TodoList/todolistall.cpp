#include <gtkmm.h>
#include <iostream>
#include <string>

// g++ project.cpp -o todo_list_gui `pkg-config --cflags --libs gtkmm-3.0`
// ./todo_list_gui

using namespace std;

class Task {
public:
    int id;
    string description;
    int priority;
    bool isDone;

    Task(int taskId, const string& taskDescription, int taskPriority)
        : id(taskId), description(taskDescription), priority(taskPriority), isDone(false) {}

    void markDone() {
        isDone = true;
    }
    bool isitDone() const {
        return isDone;
    }

    void display() const {
        cout << "Task ID: " << id << " - " << description << " [" << (isDone ? "Done" : "Not Done") << "] (Priority: " << priority << ")\n" << endl;
    }

    bool operator<(const Task& other) const {
        return priority < other.priority;
    }

    bool operator>(const Task& other) const {
        return priority > other.priority;
    }

    bool operator==(const Task& other) const {
        return id == other.id;
    }

    string toString() const {
        return "Task ID: " + to_string(id) + " - " + description + " [" + (isDone ? "Done" : "Not Done") + "] (Priority: " + to_string(priority) + ")";
    }
};

template <typename T>
class SplayTree {
private:
    struct Node {
        T data;
        Node* left;
        Node* right;

        Node(const T& value) : data(value), left(nullptr), right(nullptr) {}
    };

    Node* root;

    void rightRotate(Node*& node) {
        Node* newRoot = node->left;
        node->left = newRoot->right;
        newRoot->right = node;
        node = newRoot;
    }

    void leftRotate(Node*& node) {
        Node* newRoot = node->right;
        node->right = newRoot->left;
        newRoot->left = node;
        node = newRoot;
    }

    void splay(Node*& node, const T& value) {
        if (!node || node->data == value) return;

        if (node->data > value) {
            if (!node->left) return;
            if (node->left->data > value) {
                splay(node->left->left, value);
                rightRotate(node);
            } else if (node->left->data < value) {
                splay(node->left->right, value);
                if (node->left->right) leftRotate(node->left);
            }
            if (node->left) rightRotate(node);
        } else {
            if (!node->right) return;
            if (node->right->data > value) {
                splay(node->right->left, value);
                if (node->right->left) rightRotate(node->right);
            } else if (node->right->data < value) {
                splay(node->right->right, value);
                leftRotate(node);
            }
            if (node->right) leftRotate(node);
        }
    }

    void inOrderTraversal(Node* node, stringstream& ss) const {
        if (!node) return;
        inOrderTraversal(node->left, ss);
        ss << node->data.toString() << "\n";
        inOrderTraversal(node->right, ss);
    }

    void destroyTree(Node* node) {
        if (!node) return;
        destroyTree(node->left);
        destroyTree(node->right);
        delete node;
    }

public:
    SplayTree() : root(nullptr) {}

    ~SplayTree() {
        destroyTree(root);
    }

    void insert(const T& value) {
        if (!root) {
            root = new Node(value);
            return;
        }
        splay(root, value);
        if (root->data == value) return;
        Node* newNode = new Node(value);
        if (root->data > value) {
            newNode->right = root;
            newNode->left = root->left;
            root->left = nullptr;
        } else {
            newNode->left = root;
            newNode->right = root->right;
            root->right = nullptr;
        }
        root = newNode;
    }

    void remove(const T& value) {
        if (!root) return;
        splay(root, value);
        if (!(root->data == value)) return;
        if (!root->left) {
            Node* temp = root;
            root = root->right;
            delete temp;
        } else {
            Node* newRoot = root->left;
            splay(newRoot, value);
            newRoot->right = root->right;
            delete root;
            root = newRoot;
        }
    }

    Node* find(const T& value) {
        if (!root) return nullptr;
        splay(root, value);
        return (root->data.id == value.id) ? root : nullptr;
    }

    void display() const {
        stringstream ss;
        inOrderTraversal(root, ss);
        cout << ss.str();
    }

    string getTasksAsString() const {
        stringstream ss;
        inOrderTraversal(root, ss);
        return ss.str();
    }

    Node* getRoot() const {
        return root;
    }

    friend class ToDoList;
};

class ToDoList {
private:
    SplayTree<Task> taskTree;
    int nextId;


Task* findTaskById(SplayTree<Task>::Node* node, int taskId) const {
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

public:
    ToDoList() : nextId(1) {}

    void addTask(const string& description, int priority) {
        taskTree.insert(Task(nextId++, description, priority));
    }

    void removeTask(int taskId, bool forceRemove) {
        Task* task = findTaskById(taskTree.getRoot(), taskId);
        if (task) {
            if (task->isitDone() || forceRemove) {
                taskTree.remove(*task);
            }
        }
    }

    void markTaskDone(int taskId) {
        Task* task = findTaskById(taskTree.getRoot(), taskId);
        if (task) {
            task->markDone();
        }
    }

    string displayTasks() const {
        return taskTree.getTasksAsString();
    }

    Task getMostPrioritizedTask() const {
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
};

class ToDoListGUI : public Gtk::Window {
public:
    ToDoListGUI() : addButton("Add Task"), markDoneButton("Mark Task as Done"),
                    removeButton("Remove Task"), displayButton("Display Tasks"),
                    getPrioritizedButton("Most Prioritized Task") {
        set_title("To-Do List");
        set_default_size(400, 300);

        mainBox.pack_start(addButton);
        mainBox.pack_start(markDoneButton);
        mainBox.pack_start(removeButton);
        mainBox.pack_start(displayButton);
        mainBox.pack_start(getPrioritizedButton);

        addButton.signal_clicked().connect(sigc::mem_fun(*this, &ToDoListGUI::on_add_task));
        markDoneButton.signal_clicked().connect(sigc::mem_fun(*this, &ToDoListGUI::on_mark_done));
        removeButton.signal_clicked().connect(sigc::mem_fun(*this, &ToDoListGUI::on_remove_task));
        displayButton.signal_clicked().connect(sigc::mem_fun(*this, &ToDoListGUI::on_display_tasks));
        getPrioritizedButton.signal_clicked().connect(sigc::mem_fun(*this, &ToDoListGUI::on_get_prioritized_task));

        add(mainBox);
        show_all_children();
    }

protected:
    Gtk::Box mainBox{Gtk::ORIENTATION_VERTICAL};
    Gtk::Button addButton;
    Gtk::Button markDoneButton;
    Gtk::Button removeButton;
    Gtk::Button displayButton;
    Gtk::Button getPrioritizedButton;

    ToDoList toDoList;

    void on_add_task() {
        Gtk::Dialog dialog("Add Task", *this);
        Gtk::Box* contentArea = dialog.get_content_area();

        Gtk::Entry descriptionEntry;
        Gtk::Entry priorityEntry;

        descriptionEntry.set_placeholder_text("Task Description");
        priorityEntry.set_placeholder_text("Priority (1-10)");

        contentArea->pack_start(descriptionEntry);
        contentArea->pack_start(priorityEntry);

        dialog.add_button("Add", Gtk::RESPONSE_OK);
        dialog.add_button("Cancel", Gtk::RESPONSE_CANCEL);
        dialog.show_all_children();

        int result = dialog.run();

        if (result == Gtk::RESPONSE_OK) {
            string description = descriptionEntry.get_text();
            int priority = 0;
            try {
                priority = stoi(priorityEntry.get_text());
            } catch (invalid_argument& e) {
                Gtk::MessageDialog errorDialog(*this, "Invalid priority input. Please enter a number between 1 and 10.");
                errorDialog.run();
                return;
            }
            if (priority < 1 || priority > 10) {
                Gtk::MessageDialog errorDialog(*this, "Priority must be between 1 and 10.");
                errorDialog.run();
                return;
            }
            toDoList.addTask(description, priority);
            Gtk::MessageDialog successDialog(*this, "Task added successfully!");
            successDialog.run();
        }
    }

    void on_mark_done() {
        Gtk::Dialog dialog("Mark Task as Done", *this);
        Gtk::Box* contentArea = dialog.get_content_area();

        Gtk::Entry idEntry;
        idEntry.set_placeholder_text("Task ID");

        contentArea->pack_start(idEntry);

        dialog.add_button("Mark Done", Gtk::RESPONSE_OK);
        dialog.add_button("Cancel", Gtk::RESPONSE_CANCEL);
        dialog.show_all_children();

        int result = dialog.run();

        if (result == Gtk::RESPONSE_OK) {
            int taskId = 0;
            try {
                taskId = stoi(idEntry.get_text());
            } catch (invalid_argument& e) {
                Gtk::MessageDialog errorDialog(*this, "Invalid task ID input. Please enter a valid number.");
                errorDialog.run();
                return;
            }
            toDoList.markTaskDone(taskId);
            Gtk::MessageDialog successDialog(*this, "Task marked as done!");
            successDialog.run();
        }
    }

    void on_remove_task() {
        Gtk::Dialog dialog("Remove Task", *this);
        Gtk::Box* contentArea = dialog.get_content_area();

        Gtk::Entry idEntry;
        idEntry.set_placeholder_text("Task ID");

        contentArea->pack_start(idEntry);

        dialog.add_button("Remove", Gtk::RESPONSE_OK);
        dialog.add_button("Cancel", Gtk::RESPONSE_CANCEL);
        dialog.show_all_children();

        int result = dialog.run();

        if (result == Gtk::RESPONSE_OK) {
            int taskId = 0;
            try {
                taskId = stoi(idEntry.get_text());
            } catch (invalid_argument& e) {
                Gtk::MessageDialog errorDialog(*this, "Invalid task ID input. Please enter a valid number.");
                errorDialog.run();
                return;
            }
            toDoList.removeTask(taskId, true);
            Gtk::MessageDialog successDialog(*this, "Task removed successfully!");
            successDialog.run();
        }
    }

    void on_display_tasks() {
        Gtk::Dialog dialog("All Tasks", *this);
        Gtk::Box* contentArea = dialog.get_content_area();

        string tasks = toDoList.displayTasks();

        Gtk::Label tasksLabel(tasks);
        contentArea->pack_start(tasksLabel);

        dialog.add_button("Close", Gtk::RESPONSE_CLOSE);
        dialog.show_all_children();
        dialog.run();
    }

    void on_get_prioritized_task() {
        Task task = toDoList.getMostPrioritizedTask();
        if (task.id != 0) {
            Gtk::MessageDialog dialog(*this, "Most Prioritized Task:");
            dialog.set_secondary_text("Task ID: " + to_string(task.id) + " - " + task.description + " (Priority: " + to_string(task.priority) + ")");
            dialog.run();
        } else {
            Gtk::MessageDialog dialog(*this, "No tasks available.");
            dialog.run();
        }
    }
};

int main(int argc, char* argv[]) {
    auto app = Gtk::Application::create(argc, argv, "org.gtkmm.example");

    ToDoListGUI window;

    return app->run(window);
}

