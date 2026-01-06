#include <GL/glut.h>   // GLUT, includes glu.h and gl.h

// Function to display content
void display() {
    glClear(GL_COLOR_BUFFER_BIT);       // Clear the screen
    glBegin(GL_TRIANGLES);              // Start drawing a triangle

    glColor3f(1.0, 0.0, 0.0);           // Red
    glVertex2f(-0.5f, -0.5f);

    glColor3f(0.0, 1.0, 0.0);           // Green
    glVertex2f(0.5f, -0.5f);

    glColor3f(0.0, 0.0, 1.0);           // Blue
    glVertex2f(0.0f, 0.5f);

    glEnd();
    glFlush();                           // Render now
}

// Main function
int main(int argc, char** argv) {
    glutInit(&argc, argv);                 // Initialize GLUT
    glutCreateWindow("Simple OpenGL");     // Create window
    glutInitWindowSize(500, 500);          // Set window size
    glutDisplayFunc(display);              // Register display callback
    glutMainLoop();                        // Enter event loop
    return 0;
}
