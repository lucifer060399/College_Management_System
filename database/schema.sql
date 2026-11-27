
-- Enable foreign key constraints
PRAGMA foreign_keys = ON;


-- 1. Courses Table
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL UNIQUE,
    duration INTEGER NOT NULL CHECK (duration > 0)
);


-- 2. Students Table
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0),
    email TEXT NOT NULL UNIQUE,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);


-- 3. Subjects Table
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    UNIQUE (subject_name, course_id)
);


-- 4. Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    attendance_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Present', 'Absent')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    UNIQUE (student_id, subject_id, attendance_date)
);


-- 5. Examinations Table
CREATE TABLE IF NOT EXISTS examinations (
    exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    exam_name TEXT NOT NULL,
    max_marks REAL NOT NULL CHECK (max_marks > 0),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    UNIQUE (subject_id, exam_name)
);


-- 6. Marks Table
CREATE TABLE IF NOT EXISTS marks (
    mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    exam_id INTEGER NOT NULL,
    marks_obtained REAL NOT NULL CHECK (marks_obtained >= 0),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (exam_id) REFERENCES examinations(exam_id),
    UNIQUE (student_id, exam_id)
);


-- Create indexes for frequently searched columns
CREATE INDEX IF NOT EXISTS idx_students_course
ON students(course_id);

CREATE INDEX IF NOT EXISTS idx_subjects_course
ON subjects(course_id);

CREATE INDEX IF NOT EXISTS idx_attendance_student
ON attendance(student_id);

CREATE INDEX IF NOT EXISTS idx_attendance_date
ON attendance(attendance_date);

CREATE INDEX IF NOT EXISTS idx_marks_student
ON marks(student_id);
