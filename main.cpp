#include <windows.h>
#include <cstdio>  // 包含 sprintf 所需的头文件

int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Python executable path
    const char* pythonExe = ".\\python.exe";

    // Python script path
    const char* scriptPath = "{{{{script}}}}";

    // Command line to execute
    char cmdLine[1024];
    sprintf(cmdLine, "\"%s\" \"%s\"", pythonExe, scriptPath);

    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    // Initialize memory
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    // Hide the window
    si.dwFlags = STARTF_USESHOWWINDOW | STARTF_TITLEISLINKNAME;
    si.wShowWindow = SW_HIDE;

    // Create the process
    if (!CreateProcess(NULL,   // No module name (use command line)
                       cmdLine,        // Command line
                       NULL,           // Process handle not inheritable
                       NULL,           // Thread handle not inheritable
                       TRUE,          // Set handle inheritance to TRUE
                       // FALSE,          // Set handle inheritance to FALSE
                       CREATE_NO_WINDOW, // Creation flags to hide the window
                       NULL,           // Use parent's environment block
                       NULL,           // Use parent's starting directory
                       &si,            // Pointer to STARTUPINFO structure
                       &pi)            // Pointer to PROCESS_INFORMATION structure
    ) {
        return GetLastError();
    }

    // Wait until child process exits.
    DWORD waitResult = WaitForSingleObject(pi.hProcess, INFINITE);
    if (waitResult == WAIT_FAILED) {
        return GetLastError();
    }

    // Close process and thread handles.
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}
