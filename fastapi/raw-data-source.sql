-- Insert into kcs
INSERT INTO kcs (id, title, summary) VALUES
(1, 'Variables', 'Introducing Variables'),
(2, 'Decision Making', 'Using Boolean Algebra'),
(3, 'Looping', 'Different Types of Looping'),
(4, 'OOP', 'OOP Principles'),
(5, 'File Handling', 'Managing File Contents and Access'),
(6, 'Exception Handling', 'Different Types of Exceptions and Management');

-- Insert into dags
INSERT INTO dags (id, title, summary) VALUES
(1, 'Python Programming', 'General Programming with Python'),
(2, 'Functional Programming', 'Functional Programming and its structure');

-- Insert into dag_edges
INSERT INTO dag_edges (id, dag_id, from_kc_id, to_kc_id) VALUES
(1, 1, 1, 2),
(2, 1, 2, 3),
(3, 1, 2, 5),
(4, 1, 3, 4),
(5, 1, 4, 6),
(6, 1, 5, 6),
(7, 2, 1, 2),
(8, 2, 2, 3),
(9, 2, 3, 6),
(10, 2, 5, 6);

-- Insert Questions
INSERT INTO questions (kc_id, title, correct_option) VALUES
(1, 'What is the correct way to declare a variable in Python?', 1),
(1, 'Which keyword is used to assign a value to a variable?', 2),
(1, 'What will be the type of variable x if x = 5?', 3),

(2, 'Which operator is used for logical AND in Python?', 2),
(2, 'What is the result of True and False?', 3),
(2, 'Which statement is used for decision making in Python?', 1),

(3, 'Which loop is used to iterate over a sequence?', 2),
(3, 'What keyword is used to exit a loop early?', 4),
(3, 'What will be the output of: for i in range(3): print(i)?', 1),

(4, 'Which keyword is used to define a class in Python?', 1),
(4, 'Which method acts as a constructor in Python classes?', 2),
(4, 'What is the process of creating a new class from an existing one called?', 3),

(5, 'Which function is used to open a file in Python?', 1),
(5, 'What mode is used to append data to a file?', 4),
(5, 'Which statement is used to close a file in Python?', 2),

(6, 'Which keyword is used to handle exceptions in Python?', 1),
(6, 'What type of error occurs when dividing by zero?', 2),
(6, 'Which block is always executed whether an exception occurs or not?', 4);

-- Insert Options for each question
INSERT INTO options (question_id, [order], text) VALUES 
(1, 1, 'variable_name = value'),
(1, 2, 'declare variable_name'),
(1, 3, 'var variable_name'),
(1, 4, 'let variable_name'), 
(2, 1, 'print'),
(2, 2, '='),
(2, 3, 'let'),
(2, 4, 'var'), 
(3, 1, 'int'),
(3, 2, 'float'),
(3, 3, 'int'),
(3, 4, 'str'), 
(4, 1, '&&'),
(4, 2, 'and'),
(4, 3, '&'),
(4, 4, 'All of the above'), 
(5, 1, 'True'),
(5, 2, 'False'),
(5, 3, 'False'),
(5, 4, 'None'), 
(6, 1, 'if'),
(6, 2, 'switch'),
(6, 3, 'match'),
(6, 4, 'for'), 
(7, 1, 'while'),
(7, 2, 'for'),
(7, 3, 'do while'),
(7, 4, 'loop'), 
(8, 1, 'continue'),
(8, 2, 'pass'),
(8, 3, 'skip'),
(8, 4, 'break'), 
(9, 1, '0 1 2'),
(9, 2, '1 2 3'),
(9, 3, '0 1 2 3'),
(9, 4, 'Error'), 
(10, 1, 'class'),
(10, 2, 'def'),
(10, 3, 'struct'),
(10, 4, 'object'), 
(11, 1, '__del__'),
(11, 2, '__init__'),
(11, 3, 'constructor'),
(11, 4, 'new'), 
(12, 1, 'Encapsulation'),
(12, 2, 'Polymorphism'),
(12, 3, 'Inheritance'),
(12, 4, 'Abstraction'), 
(13, 1, 'open'),
(13, 2, 'file'),
(13, 3, 'read'),
(13, 4, 'load'), 
(14, 1, 'r'),
(14, 2, 'w'),
(14, 3, 'x'),
(14, 4, 'a'), 
(15, 1, 'stop()'),
(15, 2, 'close()'),
(15, 3, 'end()'),
(15, 4, 'exit()'), 
(16, 1, 'try'),
(16, 2, 'catch'),
(16, 3, 'handle'),
(16, 4, 'except'), 
(17, 1, 'TypeError'),
(17, 2, 'ZeroDivisionError'),
(17, 3, 'ValueError'),
(17, 4, 'IndexError'), 
(18, 1, 'try'),
(18, 2, 'except'),
(18, 3, 'catch'),
(18, 4, 'finally');
  
-- insert synthetic student data

INSERT INTO simulated_student_data (firstname, lastname, email, password, is_processed)
VALUES
('John', 'Doe', 'john.doe1@example.com', '123456', NULL),
('Jane', 'Smith', 'jane.smith2@example.com', '123456', NULL),
('Michael', 'Johnson', 'michael.johnson3@example.com', '123456', NULL),
('Emily', 'Davis', 'emily.davis4@example.com', '123456', NULL),
('Daniel', 'Brown', 'daniel.brown5@example.com', '123456', NULL),
('Sophia', 'Miller', 'sophia.miller6@example.com', '123456', NULL),
('Matthew', 'Wilson', 'matthew.wilson7@example.com', '123456', NULL),
('Olivia', 'Moore', 'olivia.moore8@example.com', '123456', NULL),
('James', 'Taylor', 'james.taylor9@example.com', '123456', NULL),
('Isabella', 'Anderson', 'isabella.anderson10@example.com', '123456', NULL),
('Ethan', 'Thomas', 'ethan.thomas11@example.com', '123456', NULL),
('Mia', 'Jackson', 'mia.jackson12@example.com', '123456', NULL),
('Alexander', 'White', 'alexander.white13@example.com', '123456', NULL),
('Charlotte', 'Harris', 'charlotte.harris14@example.com', '123456', NULL),
('Benjamin', 'Martin', 'benjamin.martin15@example.com', '123456', NULL),
('Amelia', 'Thompson', 'amelia.thompson16@example.com', '123456', NULL),
('William', 'Garcia', 'william.garcia17@example.com', '123456', NULL),
('Harper', 'Martinez', 'harper.martinez18@example.com', '123456', NULL),
('Elijah', 'Robinson', 'elijah.robinson19@example.com', '123456', NULL),
('Ava', 'Clark', 'ava.clark20@example.com', '123456', NULL);

-- insert synthetic exam data
INSERT INTO simulated_exam_data_raw (
    email, dag_title, kc_title, question, selected_option,
    time_taken, help_taken, screen_movement_weight, facial_expression_weight, is_processed
) VALUES
('john.doe1@example.com', 'Python Programming', 'Variables', 'What is the correct way to declare a variable in Python?', 'variable_name = value', 12.5, 0, 0.2, 0.1, NULL),
('jane.smith2@example.com', 'Python Programming', 'Variables', 'Which keyword is used to assign a value to a variable?', '=', 9.3, 1, 0.4, 0.2, NULL),
('michael.johnson3@example.com', 'Python Programming', 'Variables', 'What will be the type of variable x if x = 5?', 'int', 15.0, 0, 0.3, 0.3, NULL),
('emily.davis4@example.com', 'Python Programming', 'Decision Making', 'Which operator is used for logical AND in Python?', 'and', 7.8, 0, 0.1, 0.2, NULL),
('daniel.brown5@example.com', 'Python Programming', 'Decision Making', 'What is the result of True and False?', 'False', 11.4, 0, 0.5, 0.4, NULL),
('sophia.miller6@example.com', 'Python Programming', 'Decision Making', 'Which statement is used for decision making in Python?', 'if', 13.7, 1, 0.3, 0.5, NULL),
('matthew.wilson7@example.com', 'Python Programming', 'Looping', 'Which loop is used to iterate over a sequence?', 'for', 8.2, 0, 0.2, 0.1, NULL),
('olivia.moore8@example.com', 'Python Programming', 'Looping', 'What keyword is used to exit a loop early?', 'break', 10.6, 0, 0.4, 0.3, NULL),
('james.taylor9@example.com', 'Python Programming', 'Looping', 'What will be the output of: for i in range(3): print(i)?', '0 1 2', 14.0, 1, 0.2, 0.2, NULL),
('isabella.anderson10@example.com', 'Python Programming', 'OOP', 'Which keyword is used to define a class in Python?', 'class', 12.8, 0, 0.1, 0.1, NULL),
('ethan.thomas11@example.com', 'Python Programming', 'OOP', 'Which method acts as a constructor in Python classes?', '__init__', 9.9, 0, 0.3, 0.2, NULL),
('mia.jackson12@example.com', 'Python Programming', 'OOP', 'What is the process of creating a new class from an existing one called?', 'Inheritance', 11.5, 0, 0.4, 0.4, NULL),
('alexander.white13@example.com', 'Python Programming', 'File Handling', 'Which function is used to open a file in Python?', 'open', 13.1, 1, 0.3, 0.5, NULL),
('charlotte.harris14@example.com', 'Python Programming', 'File Handling', 'What mode is used to append data to a file?', 'a', 7.4, 0, 0.2, 0.3, NULL),
('benjamin.martin15@example.com', 'Python Programming', 'File Handling', 'Which statement is used to close a file in Python?', 'close()', 8.8, 0, 0.4, 0.2, NULL),
('amelia.thompson16@example.com', 'Python Programming', 'Exception Handling', 'Which keyword is used to handle exceptions in Python?', 'try', 15.2, 1, 0.3, 0.3, NULL),
('william.garcia17@example.com', 'Python Programming', 'Exception Handling', 'What type of error occurs when dividing by zero?', 'ZeroDivisionError', 9.7, 0, 0.5, 0.4, NULL),
('harper.martinez18@example.com', 'Python Programming', 'Exception Handling', 'Which block is always executed whether an exception occurs or not?', 'finally', 11.0, 0, 0.2, 0.3, NULL),
('elijah.robinson19@example.com', 'Functional Programming', 'Variables', 'What is the correct way to declare a variable in Python?', 'variable_name = value', 10.5, 0, 0.3, 0.2, NULL),
('ava.clark20@example.com', 'Functional Programming', 'Decision Making', 'Which operator is used for logical AND in Python?', 'and', 12.3, 0, 0.2, 0.3, NULL),
('john.doe1@example.com', 'Functional Programming', 'Looping', 'Which loop is used to iterate over a sequence?', 'for', 8.6, 1, 0.4, 0.4, NULL),
('jane.smith2@example.com', 'Functional Programming', 'OOP', 'Which keyword is used to define a class in Python?', 'class', 13.9, 0, 0.1, 0.1, NULL),
('michael.johnson3@example.com', 'Functional Programming', 'File Handling', 'Which function is used to open a file in Python?', 'open', 9.2, 0, 0.3, 0.2, NULL),
('emily.davis4@example.com', 'Functional Programming', 'Exception Handling', 'Which keyword is used to handle exceptions in Python?', 'try', 14.7, 1, 0.2, 0.3, NULL),
('daniel.brown5@example.com', 'Functional Programming', 'Exception Handling', 'What type of error occurs when dividing by zero?', 'ZeroDivisionError', 10.1, 0, 0.4, 0.4, NULL);





  
  