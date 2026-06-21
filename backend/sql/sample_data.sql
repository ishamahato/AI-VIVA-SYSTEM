-- Sample question data (reference).
-- NOTE: user accounts need bcrypt-hashed passwords, so create them with
--       `python seed.py` rather than raw SQL. These questions assume a
--       faculty row with id = 1 exists (seed.py creates one).

INSERT INTO questions (subject, text, difficulty, expected_answer, keywords, created_by) VALUES
('Database', 'What is database normalization and why is it important?', 'medium',
 'Normalization organizes data to reduce redundancy and improve integrity (1NF, 2NF, 3NF) and prevents anomalies.',
 'redundancy, integrity, 1NF, 2NF, 3NF, anomalies', 1),
('Database', 'Explain the difference between a primary key and a foreign key.', 'easy',
 'A primary key uniquely identifies a row and cannot be null; a foreign key references another table''s primary key for referential integrity.',
 'primary key, foreign key, unique, referential integrity', 1),
('Operating Systems', 'What is a deadlock and what are its four necessary conditions?', 'hard',
 'A deadlock is processes waiting on each other forever. Conditions: mutual exclusion, hold and wait, no preemption, circular wait.',
 'mutual exclusion, hold and wait, no preemption, circular wait', 1),
('Networking', 'Explain the difference between TCP and UDP.', 'medium',
 'TCP is connection-oriented and reliable; UDP is connectionless and faster with no delivery guarantee.',
 'TCP, UDP, connection-oriented, reliable, connectionless', 1);
