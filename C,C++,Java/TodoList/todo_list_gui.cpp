#include "todo_list_gui.h"

ToDoListGUI::ToDoListGUI() : addButton("Add Task"), markDoneButton("Mark Task as Done"),
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

void ToDoListGUI::on_add_task() {
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
        std::string description = descriptionEntry.get_text();
        int priority = 0;
        try {
            priority = std::stoi(priorityEntry.get_text());
        } catch (std::invalid_argument& e) {
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

void ToDoListGUI::on_mark_done() {
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
            taskId = std::stoi(idEntry.get_text());
        } catch (std::invalid_argument& e) {
            Gtk::MessageDialog errorDialog(*this, "Invalid task ID input. Please enter a valid number.");
            errorDialog.run();
            return;
        }
        toDoList.markTaskDone(taskId);
        Gtk::MessageDialog successDialog(*this, "Task marked as done!");
        successDialog.run();
    }
}

void ToDoListGUI::on_remove_task() {
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
            taskId = std::stoi(idEntry.get_text());
        } catch (std::invalid_argument& e) {
            Gtk::MessageDialog errorDialog(*this, "Invalid task ID input. Please enter a valid number.");
            errorDialog.run();
            return;
        }
        toDoList.removeTask(taskId, true);
        Gtk::MessageDialog successDialog(*this, "Task removed successfully!");
        successDialog.run();
    }
}

void ToDoListGUI::on_display_tasks() {
    Gtk::Dialog dialog("All Tasks", *this);
    Gtk::Box* contentArea = dialog.get_content_area();

    std::string tasks = toDoList.displayTasks();

    Gtk::Label tasksLabel(tasks);
    contentArea->pack_start(tasksLabel);

    dialog.add_button("Close", Gtk::RESPONSE_CLOSE);
    dialog.show_all_children();
    dialog.run();
}

void ToDoListGUI::on_get_prioritized_task() {
    Task task = toDoList.getMostPrioritizedTask();
    if (task.id != 0) {
        Gtk::MessageDialog dialog(*this, "Most Prioritized Task:");
        dialog.set_secondary_text("Task ID: " + std::to_string(task.id) + " - " + task.description + " (Priority: " + std::to_string(task.priority) + ")");
        dialog.run();
    } else {
        Gtk::MessageDialog dialog(*this, "No tasks available.");
        dialog.run();
    }
}
