#voiceRec_test
import unittest
import speech_recognition as sr
import subprocess
import re
import json
import sys
from API.app import app as a
from masterPi_voiceSearch import AdminUser as vs

class TestVoiceRec(unittest.TestCase):
    
    def test_extraCommand(self):
        #expect pass
        result = vs.getCommand('search for user 1234 please and thankyou')
        self.assertEqual(result, 'user')
        
    def test_exactCommand(self):
        #expect pass
        result = vs.getCommand('search for available')
        self.assertEqual(result, 'available')
        
    @unittest.expectedFailure
    def test_wrongCommand(self):
        #expect fail
        result = vs.getCommand('give me available cars')
        self.assertEqual(result, 'available')
        
    def test_extraVar(self):
        #expect pass
        result = vs.getVar('quick brown fox jumps over the lazy dog', 2)
        self.assertEqual(result, 'fox')
        
    def test_exactVar(self):
        #expect pass
        result = vs.getVar('quick brown fox jumps over the lazy dog', 7)
        self.assertEqual(result, 'dog')
        
    @unittest.expectedFailure
    def test_outOfBoundsVar(self):
        #expect fail
        result = vs.getVar('quick brown fox jumps over the lazy dog', 8)
        self.assertEqual(result, 'dog')