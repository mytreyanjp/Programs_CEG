#ifndef TODOLISTGUI_H
#define TODOLISTGUI_H

#include <gtkmm.h>
#include "todolist.h"

class ToDoListGUI : public Gtk::Window {
public:
    ToDoListGUI();

protected:
    Gtk::Box mainBox{Gtk::ORIENTATION_VERTICAL};
    Gtk::Button addButton;
    Gtk::Button markDoneButton;
    Gtk::Button removeButton;
    Gtk::Button displayButton;
    Gtk::Button getPrioritizedButton;

    ToDoList toDoList;

    void on_add_task();
    void on_mark_done();
    void on_remove_task();
    void on_display_tasks();
    void on_get_prioritized_task();
};

#endif // TODOLISTGUI_H
