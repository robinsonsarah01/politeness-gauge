from javax.swing import JButton, JPanel, JTextArea, JTextField, JFrame, JLabel
from java.awt import GridLayout, BorderLayout #, Color
import measurements as mes
# from java.awt.event import ActionEvent, ActionListener

class gui(JFrame):
    def __init__(self):

        #Class variable declarations
        self.mainPanel = JPanel(GridLayout(1,2))
        self.subPanel1 = JPanel(BorderLayout())
        self.subPanel2 = JPanel(GridLayout(5,1))
        
        self.userText = JTextArea(' ')
        
        self.emoticonFeedback = JTextArea('This will consider your emoticon usage.')
        self.curseFeedback = JTextArea('This will consider your use of profanity.')
        self.styleFeedback = JTextArea('This will consider your general tone.')
        self.overallFeedback = JTextArea('This will be your overall score.')
        
        self.button = JButton("Score my email!",
        						actionPerformed=self.updateScores)
        
        self.initGUI()
        self.add(self.mainPanel)
        
        self.setSize(800, 500)
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setVisible(True)

    def initGUI(self):
        #Set up subpanel1
        appName = JTextArea('Politeness Gauge\n'+'\nSarah Robinson \nAnna Clegg')
        appName.setLineWrap(True)
        appName.setWrapStyleWord(True)
        appName.setEditable(False)
        appName.background =  240,240,240
        instructions = JTextArea('   Ever agonized over whether or not your emails' +
                    ' are polite enough? \n    Never fear! With our politeness gauge' +
                    ' we can provide suggestions on improving your emails' +
                    ' with just the click of a button.  \n    Just type your email ' +
                    'into the text box below and hit Score!')
        instructions.setLineWrap(True)
        instructions.setWrapStyleWord(True)
        instructions.background = 240,240,240
        northPanel = JPanel(GridLayout(2,1))
        northPanel.add(appName)
        northPanel.add(instructions)
        self.subPanel1.add(northPanel, BorderLayout.NORTH)  
        
        self.userText.setEditable(True)
        self.userText.setLineWrap(True)
        self.userText.setWrapStyleWord(True)
        self.userText.setRows(100)
        #self.userText.wordWrap = True
        self.subPanel1.add(self.userText, BorderLayout.CENTER)
        
        self.subPanel1.add(self.button, BorderLayout.SOUTH)
        
        label = JLabel("Politeness Evaluation")
        self.subPanel2.add(label)
        self.subPanel2.add(self.emoticonFeedback)
        self.subPanel2.add(self.curseFeedback)
        self.subPanel2.add(self.styleFeedback)
        self.subPanel2.add(self.overallFeedback)
        
        self.mainPanel.add(self.subPanel1)
        self.mainPanel.add(self.subPanel2)
        
        
    def updateScores(self, event):
    	input = self.userText.getText()
    	scores = mes.get_scores(input)
    	overall = mes.get_overall_score()
    	
    	self.styleFeedback.setText("\n Your politeness score is "+str(scores['politeness'])
    								+".\n Higher is better. This is relative to the\n length of your email,"
    								+" so the more sentences you have,\n the higher this score should be.")
    								
        self.curseFeedback.setText(" You have about " +str(scores['curses'])+" curses in you email."
        								+"\n Please try to have 0 curses.")
        self.emoticonFeedback.setText(" You have about "+str(scores['emoticons'])+" emoticons in your email."
        								+"\n Fewer emoticons is considered more professional.")
        								
        self.overallFeedback.setText(" Your overall professionality score is "+str(overall)+"."
        							+"\n The baseline is around 50 for neutral emails."
        							+"\n Please remember that this is approximate.")
    	
        

if __name__ == '__main__':
    gui()
        