from pylatex import Document, Section, NoEscape, MiniPage, Command
import pylatex
from question.models import Question
from assignment.models import Assignment
from django.conf import settings
from pylatex.utils import escape_latex
import re


def generate_assignment_pdf(assignment, questions, university_name, university_logo):
    try:
        # Create a new document
        # doc = Document()
        doc = Document(geometry_options={"margin": "2cm"})
        doc.packages.append(pylatex.Package("graphicx"))
        doc.packages.append(pylatex.Package("listings"))
        latex_dir = os.path.join(settings.BASE_DIR, "latex")
        os.makedirs(latex_dir, exist_ok=True)

        # Configure listings for code blocks
        doc.append(NoEscape(r"\lstset{basicstyle=\ttfamily\small,breaklines=true}"))

        # Resolve and validate university logo path
        logo_abs_path = os.path.join(latex_dir, university_logo)
        if not os.path.exists(logo_abs_path):
            raise FileNotFoundError(f"University logo not found at {logo_abs_path}")

        # Helpers to format markdown into LaTeX
        def choose_verb_delimiter(text: str) -> str:
            for delim in ['|', '!', '#', '/', '+', '~', '@', '%', ';', ':']:
                if delim not in text:
                    return delim
            return '|'  # fallback

        def format_inline(text: str) -> str:
            # Replace inline code `code` with \verb|code|
            def repl_code(m):
                content = m.group(1)
                d = choose_verb_delimiter(content)
                return f"\\verb{d}{content}{d}"

            # Replace bold **text** with \textbf{text}, escaping inside
            def repl_bold(m):
                content = m.group(1)
                return f"\\textbf{{{escape_latex(content)}}}"

            # Process sequentially: split by inline code first to avoid escaping its content
            parts = []
            last = 0
            for m in re.finditer(r"`([^`]+)`", text):
                parts.append(escape_latex(text[last:m.start()]))
                parts.append(repl_code(m))
                last = m.end()
            parts.append(escape_latex(text[last:]))
            text_escaped = "".join(parts)
            # Now bold on the escaped text (safe)
            text_escaped = re.sub(r"\*\*(.+?)\*\*", repl_bold, text_escaped)
            return text_escaped

        def markdown_to_latex(md: str) -> str:
            if not md:
                return ""
            out = []
            i = 0
            code_block_pattern = re.compile(r"```(\w+)?\n([\s\S]*?)```", re.MULTILINE)
            for m in code_block_pattern.finditer(md):
                # Text before code block
                out.append(format_inline(md[i:m.start()]))
                lang = m.group(1) or ""
                code = m.group(2)
                lang_opt = f"[language={lang.capitalize()}]" if lang else ""
                out.append("\n\\begin{lstlisting}%s\n%s\n\\end{lstlisting}\n" % (lang_opt, code))
                i = m.end()
            # Remainder text
            out.append(format_inline(md[i:]))
            return "".join(out)

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

        with doc.create(MiniPage(width=r"0.6\linewidth")):
            doc.append(NoEscape(r"\begin{flushleft}"))
            # Left Column: Course name, assignment type, professor name
            doc.append(NoEscape(r"\large{Course: \textbf{%s}}" % escape_latex(assignment.course.name)))
            doc.append(Command("vspace", "0.1cm"))
            doc.append(Command("newline"))
            doc.append(Command("vspace", "0.1cm"))
            # doc.append(Command('vspace', '0.3cm'))
            doc.append(
                NoEscape(
                    r"\normalsize{Professor: \textbf{%s}}"
                    % escape_latex(assignment.course.professor_name)
                )
            )
            doc.append(Command("newline"))
            doc.append(Command("vspace", "0.1cm"))
            # doc.append(Command('vspace', '0.3cm'))
            doc.append(
                NoEscape(
                    r"\normalsize{\textbf{%s} assignment}" % escape_latex(assignment.assignment_type)
                )
            )
            doc.append(NoEscape(r"\end{flushleft}"))

        with doc.create(MiniPage(width=r"0.36\linewidth")):
            doc.append(NoEscape(r"\begin{flushright}"))
            doc.append(
                Command(
                    "includegraphics", options="width=1.75cm", arguments=university_logo
                )
            )
            doc.append(
                NoEscape(r"\hfill")
            )  # Add horizontal space to push content to the right
            doc.append(Command("newline"))
            doc.append(NoEscape(r"\hfill"))
            doc.append(
                Command(
                    "textbf", arguments=Command("normalsize", arguments=escape_latex(university_name))
                )
            )
            doc.append(NoEscape(r"\end{flushright}"))

        doc.append(NoEscape(r"\begin{center}"))
        doc.append(NoEscape(r"\hrule height 0.02cm"))
        doc.append(Command("vspace", "0.2cm"))
        doc.append(NoEscape(r"\large{\textbf{%s}}" % escape_latex(assignment.title)))
        doc.append(Command("vspace", "0.2cm"))
        doc.append(NoEscape(r"\hrule height 0.02cm"))
        doc.append(NoEscape(r"\end{center}"))

        # Helper to map attachment URL to a relative LaTeX path and absolute FS path under latex dir
        def map_url_to_latex_paths(url: str):
            if url is None:
                return None, None
            clean = url.lstrip("/")
            # Case: starts with latex/
            if clean.startswith("latex/"):
                rel = clean[len("latex/"):]
                return f"./{rel}", os.path.join(latex_dir, rel)
            # Case: starts directly with questionattachments/
            if clean.startswith("questionattachments/"):
                rel = clean
                return f"./{rel}", os.path.join(latex_dir, rel)
            # Fallback: try to use basename under questionattachments
            basename = os.path.basename(clean)
            rel = f"questionattachments/{basename}"
            return f"./{rel}", os.path.join(latex_dir, rel)

        # Add questions
        for idx, question in enumerate(
            questions.filter(is_selected_for_assignment=True).order_by("order"), start=1
        ):
            with doc.create(Section(NoEscape(r"\textbf{%s}" % escape_latex(question.title)))):
                # Question details (supports markdown inline/bold/code blocks)
                formatted = markdown_to_latex(question.details_modified)
                doc.append(NoEscape(formatted))
                # Add attachment if available
                if question.attachment:
                    rel_tex_path, abs_fs_path = map_url_to_latex_paths(getattr(question.attachment, "url", None))
                    if not abs_fs_path or not os.path.exists(abs_fs_path):
                        raise FileNotFoundError(f"Attachment not found for question '{question.title}': expected at {abs_fs_path}")
                    doc.append(NoEscape(r"\begin{center}"))
                    doc.append(
                        Command(
                            "includegraphics",
                            options="width=8cm",
                            arguments=rel_tex_path,
                        )
                    )
                    doc.append(NoEscape(r"\end{center}"))
                    # doc.append(NoEscape(r'\textbf{Attachment:} %s' % question.attachment.url))

        # Generate PDF at absolute path inside the project latex folder
        output_base = os.path.join(settings.BASE_DIR, "latex", "assignment_pdf")
        try:
            doc.generate_pdf(output_base, clean_tex=False)
        except Exception as e:
            # Attach relevant tail of the LaTeX log for easier debugging
            log_path = f"{output_base}.log"
            log_tail = ""
            try:
                if os.path.exists(log_path):
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        tail_lines = lines[-80:]
                        log_tail = "".join(tail_lines)
            except Exception:
                # Ignore secondary errors while trying to read logs
                pass
            raise RuntimeError(f"LaTeX compilation failed: {e}\n--- assignment_pdf.log (tail) ---\n{log_tail}")
        return os.path.join(settings.BASE_DIR, "latex", "assignment_pdf.pdf")
    except Exception as e:
        # Re-raise so the API layer can return a proper error
        raise


from core.models import Course
import os


def remove_files_in_latex_folder():
    # Define the directory path
    latex_folder = os.path.join(settings.BASE_DIR, "latex")

    try:
        # Ensure the latex directory exists
        os.makedirs(latex_folder, exist_ok=True)
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

    # Retrieve Assignment
    try:
        assignment = Assignment.objects.get(id=assignment_id)
    except Assignment.DoesNotExist:
        raise ValueError(f"Assignment with ID {assignment_id} does not exist.")

    # Retrieve questions associated with Assignment
    questions = Question.objects.filter(assignment_id=assignment_id, is_selected_for_assignment=True)
    print(len(questions))

    # University details
    university_name = "Sharif University of Technology"
    university_logo = "logo.png"  # Expected to be inside the latex directory

    # Call generate_assignment_pdf function
    pdf_path = generate_assignment_pdf(assignment, questions, university_name, university_logo)

    # Verify the PDF exists before returning success
    if not os.path.exists(pdf_path):
        raise RuntimeError("PDF generation reported success but the file was not found.")
    return pdf_path


# Call the function to retrieve Assignment 1 and generate the PDF
# retrieve_and_generate_pdf()
