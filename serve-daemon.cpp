#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <cstdio>
#include <iomanip>
#include <cstring>

std::string pad(const char* serverid, const char* msgid) {

    std::stringstream ss;
    ss << "db/" << "server/" << std::string(serverid) << "/";
    ss << std::setfill('0') << std::setw(16) << std::string(msgid);
    std::string loc = ss.str();

    return loc;    

}

void read(const char* serverid, const char* msgid) {
    
    std::string loc = pad(serverid, msgid);
    std::ifstream fis;
    std::vector<std::string> out = {};

    fis.open(loc);
    if (!fis.is_open()) {
        std::cerr << "404 not found";
    } else {
        std::string line;
        while (std::getline(fis, line)) {
            std::cout << line << "\n";
        }
    }
}

void write(const char* serverid, const char* msgid, std::string user, std::string date, std::string title, std::string body) {
    
    std::string loc = pad(serverid, msgid);
    std::ofstream fis(loc);
    fis << user << "" << date << "" << title << "" << body << "";

}

/* unused

std::vector<std::string> split(std::string inp, char del) {

    std::vector<std::string> out;
    std::string emptystr = "";
    out.push_back(emptystr);
    unsigned i = 0;
    
    for (int j=0; j<inp.length(); j++) {
        if (inp[j] == del) {
            out.push_back(emptystr);
            i++;
        } else {
            out[i] = out[i] + inp[j];
        }
    }

    return out;

}

*/

int main(int argc, char* argv[]) {
    
    if (strcmp(argv[1], "read") == 0) {

        const char* serverid = argv[2];
        const char* msgid = argv[3];
        read(serverid, msgid);
        
    } else if (strcmp(argv[1], "write") == 0) {

        const char* serverid = argv[2];
        const char* msgid = argv[3];
        const char* user = argv[4];
        const char* date = argv[5];
        const char* title = argv[6];
        const char* body = argv[7];
        write(serverid, msgid, user, date, title, body);

    }

    return 0;

}