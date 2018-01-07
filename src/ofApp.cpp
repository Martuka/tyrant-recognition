#include "ofApp.h"


int CAM_WIDTH = 640;
int CAM_HEIGHT = 480;
int FONT_SIZE = 30;
int WIDTH;
int HEIGHT;
int MARGIN = 30;
int RES_WIDTH = 210;
int RES_HEIGHT = 300;

bool first = true;
bool ready = false;

string subject_picture_path = "tmp/subject.png";

//--------------------------------------------------------------
void ofApp::setup() {
    ofSetDataPathRoot("../Resources/data/");
    daFont.load("font/HELR45W.ttf", FONT_SIZE);
    camClick.load("sound/camera-click.wav");
    camClick.setVolume(0.1);
    cam.setPixelFormat(OF_PIXELS_RGB);
    cam.setup(CAM_WIDTH, CAM_HEIGHT);
    WIDTH = ofGetWindowWidth();
    HEIGHT = ofGetWindowHeight();

    takePicBtn.addListener(this, &ofApp::takePictureButtonPressed);
    performBtn.addListener(this, &ofApp::performFacialRec);

    panel1.setup("", "", 2*MARGIN, MARGIN + 260);
    panel1.add(takePicBtn.setup("Take picture"));
    imageArray64.reserve(64);


}

//--------------------------------------------------------------
void ofApp::update() {
    cam.update();
}

//--------------------------------------------------------------
void ofApp::draw() {
    WIDTH = ofGetWindowWidth();
    HEIGHT = ofGetWindowHeight();


    int cam_w = 320;
    int cam_h = 240;

    float SPACE = HEIGHT / 100;

    float x_start = MARGIN + cam_w + 3.5*MARGIN;
    float x_end = WIDTH - MARGIN - RES_WIDTH - MARGIN;
    float matrix_x = x_end - x_start;

    float y_start = MARGIN;
    float y_end = HEIGHT - 3*MARGIN;
    float matrix_y = y_end - y_start;
    float micro_margin = 8;

    float pic_w = min(((matrix_x - 7 * micro_margin) / 8), ((matrix_y - 7 * micro_margin) / 8));
    float pic_h = pic_w;

    float result_margin = 20;

    float result_h = (matrix_y - 3 * result_margin) / 4;
    float result_w = result_h;

    ofBackground(127, 127, 127);

    cam.draw(2*MARGIN, MARGIN, cam_w, cam_h);

    panel1.draw();
    if (!first) {
        subjectImage.draw(2*MARGIN, MARGIN + 260, cam_w, cam_h);
        panel2.draw();
    }

    if (ready) {
        int W = WIDTH;
        int H = HEIGHT;
        int k = 0;
        // drawing of 64 squared pictures
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                int pos_x = x_start + j*pic_w + j*micro_margin;
                int pos_y = y_start + i*pic_h + i*micro_margin;
                imageArray64[k]->image.draw(pos_x, pos_y, pic_w, pic_h);
                k++;
            }
        }
        // drawing of 4 results, firsts of the 64 previous
        for (int i = 0; i < 4; i++) {
            int pos_x = WIDTH - 2*MARGIN - result_w;
            int pos_y = i+1 * MARGIN + i * result_h + i * MARGIN;
            imageArray64[i]->image.draw(pos_x, pos_y, result_w, result_h);
            ofDrawBitmapStringHighlight(imageArray64[i]->tyrant + " " + imageArray64[i]->name, pos_x, pos_y + result_h);
            ofDrawBitmapStringHighlight("delta: " + imageArray64[i]->delta, pos_x, pos_y + result_h + 20);
        }
    }
}

//--------------------------------------------------------------
template<typename Out>
void split(const string &s, char delim, Out result) {
    stringstream ss(s);
    string item;
    while (getline(ss, item, delim)) {
        *(result++) = item;
    }
}

vector<string> split(const string &s, char delim) {
    vector<string> elems;
    split(s, delim, std::back_inserter(elems));
    return elems;
}

ofApp::Picture* process(string* line) {
    cout << "line read: " << *line << endl;
    vector<string> elems = split(*line, ' ');
    vector<string> names = split(elems[1], '_');
    ofApp::Picture *pic = new ofApp::Picture();
    pic->image.load(elems[0]);
    for (int i = 0; i < names.size() - 1; i++) {
        pic->name += names[i] + " ";
    }
    pic->name += names[names.size() - 1];
    pic->tyrant = elems[2] == "Dictateurs" ? "Dictator" : "Nobel Peace";
    pic->delta = elems[3];

    return pic;
}

void ofApp::generateAverage() {
    string command = "/usr/local/bin/python3 " +
    ofToDataPath("average.py ", true) +
    ofToDataPath("tmp ", true) +
    ofToDataPath("&");

    system(command.c_str());
}

void ofApp::keyPressed(int key) {
    if (key == 'p') {
        takePictureButtonPressed();
    }
    if (key == ' ') {
        performFacialRec();
        generateAverage();
    }
}

void ofApp::takePictureButtonPressed() {
    if (cam.isInitialized()) {
        camClick.play();
        subjectImage.setFromPixels(cam.getPixels());
        subjectImage.save(subject_picture_path);
    }
    if (first) {
        panel2.setup("", "", 2*MARGIN, MARGIN + 260 + 260);
        panel2.add(performBtn.setup("Search!"));
//        panel1.add(performBtn.setup("Search!"));
        panel1.setPosition(2*MARGIN, MARGIN + 260 + 240);
        first = false;
    }
}

void ofApp::performFacialRec() {
    string command = "/usr/local/bin/python3 " +
    ofToDataPath("main.py ", true) +
    ofToDataPath(subject_picture_path, true);

    system(command.c_str());
    string line;

    string filename("data/results.txt");
    cout << "* trying to open and read: " << filename << endl;
    ifstream f ("data/results.txt");

    if (!f.is_open())
        perror(("error while opening file " + filename).c_str());

    int i = 0;
    int j = 0;
    int k = 0;
    while (getline(f, line)) {
        imageArray64[i++] = process(&line);
    }

    if (f.bad())
        perror(("error while reading file " + filename).c_str());
    f.close();
    onResultReady();
}

void ofApp::onResultReady() {
    ready = true;
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){
    WIDTH = w;
    HEIGHT = h;
}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}
