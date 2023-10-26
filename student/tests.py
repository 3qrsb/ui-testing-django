from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
import time

option = webdriver.EdgeOptions()
driver = webdriver.Edge(options = option)
driver.get("http://127.0.0.1:8000/student/")

add = driver.find_element(By.LINK_TEXT, "Add Student")
add.click()

name = driver.find_element(By.NAME, "name")
name.send_keys("Joe")
age = driver.find_element(By.NAME, "age")
age.send_keys("20")
section = driver.find_element(By.NAME, "section")
section.send_keys("AO")
print(name)
print(age)
print(section)
time.sleep(3)
modify = driver.find_element(By.NAME, "button")
modify.click()

time.sleep(3)

class StudentCRUDTests(LiveServerTestCase):
    def test_delete_student(self):
        
        driver.get("http://127.0.0.1:8000/student/19/delete")
        self.assertIn("Delete Record", driver.title)

        # Check if the "Delete" button is present
        delete_button = driver.find_element(By.XPATH, '//button[contains(@name, "Delete")][contains(@value, "Delete")][contains(@class, "btn btn-warning")]')
        self.assertIsNotNone(delete_button)

        # Perform the delete action
        delete_button.click()

        # Wait for a brief moment to let the delete action complete (adjust the wait time if necessary)
        time.sleep(3)

        # Check if the student has been deleted
        driver.get(self.live_server_url + '/student/')  # Navigate to the student list page
        student_names = driver.find_elements(By.XPATH, '//td[contains(@class, "name")]')
        student_names = [name.text for name in student_names]
        self.assertNotIn("Joe", student_names)
        time.sleep(3)


    def test_update_student(self):
        driver.get("http://127.0.0.1:8000/student/")
        self.assertIn("Registeration of Students", driver.title)

        # Check if there are students listed
        students = driver.find_elements(By.TAG_NAME, 'tr')

        # Assuming you have at least one student to update
        if len(students) > 1:
            # Click the "Edit" button of the first student in the table
            edit_button = students[1].find_element(By.PARTIAL_LINK_TEXT, "Edit")
            edit_button.click()

            # Check if we are on the update page


            # Find the form input fields by name and update the student information
            name_input = driver.find_element(By.NAME, "name")
            name_input.clear()
            name_input.send_keys("Updated")

            section_input = driver.find_element(By.NAME, "section")
            section_input.clear()
            section_input.send_keys("Updated")

            age_input = driver.find_element(By.NAME, "age")
            age_input.clear()
            age_input.send_keys("25")

            # Submit the form
            submit_button = driver.find_element(By.NAME, "button")
            submit_button.click()

            # Check if we are redirected back to the student list page
            self.assertIn("Registeration of Students", driver.title)

            # Check if the student's information has been updated
            updated_student = driver.find_element(By.XPATH, f'//td[text()="Updated"]')
            self.assertIsNotNone(updated_student)
        else:
            self.skipTest("No students available for update")
driver.quit