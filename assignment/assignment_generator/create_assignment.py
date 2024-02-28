from pylatex import Document, Section, NoEscape, MiniPage, Command
import pylatex
from question.models import Question
from assignment.models import Assignment

def generate_assignment_pdf(assignment, questions, university_name, university_logo):
    # Create a new document
    # doc = Document()
    doc = Document(geometry_options={"margin": "2cm"})
    doc.packages.append(pylatex.Package('graphicx'))

    # Add header with university logo, name, professor, etc.
    # with doc.create(Section('')):
    # doc.append(NoEscape(r'\hrule'))
    # doc.append(NoEscape(r'\begin{center}'))
    # # Include university logo
    # doc.append(NoEscape(r'\includegraphics[width=2cm]{%s}' % university_logo))
    # doc.append(NoEscape(r'\vspace{0.5cm}'))  # Adjust vertical space
    # # University name
    # doc.append(NoEscape(r'\textbf{\LARGE %s}' % university_name))
    # doc.append(NoEscape(r'\vspace{0.3cm}'))  # Adjust vertical space
    # doc.append(NoEscape(r'\vspace{0.3cm}'))  # Adjust vertical space
    # # Professor name
    # doc.append(NoEscape(r'\textbf{Professor:} %s' % professor_name))
    # doc.append(NoEscape(r'\vspace{0.3cm}'))  # Adjust vertical space
    # # Course details
    # doc.append(NoEscape(r'\textbf{Course:} %s' % assignment.course.name))
    # doc.append(NoEscape(r'\vspace{0.3cm}'))  # Adjust vertical space
    # # Assignment type and title
    # doc.append(NoEscape(r'\textbf{Assignment Type:} %s' % assignment.assignment_type))
    # doc.append(NoEscape(r'\vspace{0.3cm}'))  # Adjust vertical space
    # doc.append(NoEscape(r'\textbf{Title:} %s' % assignment.title))
    # doc.append(NoEscape(r'\vspace{0.5cm}'))
    # doc.append(NoEscape(r'\hrule'))
    # doc.append(NoEscape(r'\end{center}'))
    
    with doc.create(MiniPage(width=r'0.6\linewidth')):
        doc.append(NoEscape(r'\begin{flushleft}'))
        # Left Column: Course name, assignment type, professor name
        doc.append(NoEscape(r'\large{Course: \textbf{%s}}' % assignment.course.name))
        doc.append(Command('vspace', '0.1cm'))
        doc.append(Command('newline'))
        doc.append(Command('vspace', '0.1cm'))
        # doc.append(Command('vspace', '0.3cm'))
        doc.append(NoEscape(r'\normalsize{Professor: \textbf{%s}}' % assignment.course.professor_name))
        doc.append(Command('newline'))
        doc.append(Command('vspace', '0.1cm'))
        # doc.append(Command('vspace', '0.3cm'))
        doc.append(NoEscape(r'\normalsize{\textbf{%s} assignment}' % assignment.assignment_type))
        doc.append(NoEscape(r'\end{flushleft}'))

    
    with doc.create(MiniPage(width=r'0.36\linewidth')):
        doc.append(NoEscape(r'\begin{flushright}'))
        doc.append(Command('includegraphics', options='width=1.75cm', arguments=university_logo))
        doc.append(NoEscape(r'\hfill'))  # Add horizontal space to push content to the right
        doc.append(Command('newline'))
        doc.append(NoEscape(r'\hfill'))
        doc.append(Command('textbf', arguments=Command('normalsize', arguments=university_name)))
        doc.append(NoEscape(r'\end{flushright}'))


    doc.append(NoEscape(r'\begin{center}'))
    doc.append(NoEscape(r'\hrule height 0.02cm'))
    doc.append(Command('vspace', '0.2cm'))
    doc.append(NoEscape(r'\large{\textbf{%s}}' % assignment.title))
    doc.append(Command('vspace', '0.2cm'))
    doc.append(NoEscape(r'\hrule height 0.02cm'))
    doc.append(NoEscape(r'\end{center}'))
    
    # Add questions
    for idx, question in enumerate(questions.filter(is_selected_for_assignment=True).order_by('order'), start=1):
        with doc.create(Section(NoEscape(r'\textbf{%s}' % question.title))):
            # Question details
            doc.append(NoEscape(r'%s' % question.details_modified))
            # Add attachment if available
            if question.attachment:
                doc.append(NoEscape(r'\begin{center}'))
                doc.append(Command('includegraphics', options='width=8cm', arguments=question.attachment.url.replace("/latex/", "./")))
                doc.append(NoEscape(r'\end{center}'))
                # doc.append(NoEscape(r'\textbf{Attachment:} %s' % question.attachment.url))

    # Generate PDF
    doc.generate_pdf('latex/assignment_pdf', clean_tex=False)

    return doc.dumps()
    
    
from user.models import Course
import os

def remove_files_in_latex_folder():
    # Define the directory path
    latex_folder = "latex"

    try:
        # Get a list of all files and directories in the latex folder
        files_in_folder = os.listdir(latex_folder)

        # Iterate over each file in the folder
        for file_name in files_in_folder:
            # Construct the full path to the file
            if file_name == "logo.png":
                continue
            file_path = os.path.join(latex_folder, file_name)

            # Check if the path points to a file (not a directory)
            if os.path.isfile(file_path):
                # Remove the file
                os.remove(file_path)
                print(f"Removed: {file_path}")
            else:
                # Optionally, you can add handling for directories if needed
                pass

        print("All files in the latex folder have been removed successfully.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")



def retrieve_and_generate_pdf(assignment_id):
    # Call the function to remove files in the latex folder
    remove_files_in_latex_folder()

    # Retrieve Assignment 1
    try:
        assignment = Assignment.objects.get(id=assignment_id)
    except Assignment.DoesNotExist:
        print("Assignment with ID 1 does not exist.")
        return

    # Retrieve questions associated with Assignment 1
    questions = Question.objects.filter(assignment=assignment)

    # University details
    university_name = "Sharif University of Technology"
    university_logo = "logo.png"  # Provide the path to your university logo

    # Call generate_assignment_pdf function
    generate_assignment_pdf(assignment, questions, university_name, university_logo)

# Call the function to retrieve Assignment 1 and generate the PDF
# retrieve_and_generate_pdf()