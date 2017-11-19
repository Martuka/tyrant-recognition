#pragma once

#include "ofMain.h"
#include "ofxGui.h"
#include <string>
#include <sstream>
#include <vector>
#include <iterator>

class ofApp : public ofBaseApp{

public:
	void setup();
	void update();
	void draw();

	void keyPressed(int key);
	void keyReleased(int key);
	void mouseMoved(int x, int y );
	void mouseDragged(int x, int y, int button);
	void mousePressed(int x, int y, int button);
	void mouseReleased(int x, int y, int button);
	void mouseEntered(int x, int y);
	void mouseExited(int x, int y);
	void windowResized(int w, int h);
	void dragEvent(ofDragInfo dragInfo);
	void gotMessage(ofMessage msg);

    void takePictureButtonPressed();
    void performButtonPressed();

    void onResultReady();

    struct Pictures {
        ofImage image;
        string name;
        string delta;
    };

    vector<string> matchesPaths;
    vector<string> deltas;
    vector<string> photos;
    vector<ofImage> matches;
    vector<Pictures*> imageArray64;
    ofTrueTypeFont daFont;
    ofSoundPlayer camClick;
    ofVideoGrabber cam;
    ofTexture subjectTexture;
    ofImage subjectImage;

    ofxButton takePicBtn;
    ofxButton performBtn;
    ofxPanel panel1;
    ofxPanel panel2;

};