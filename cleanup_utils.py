import sys

with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\utils.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('    # --- ACTIVE LEGAL VIEW RENDERER ---')
if start_idx != -1:
    end_idx = content.find('    st.markdown("""\n    <div style="background: #050508;', start_idx)
    if end_idx != -1:
        new_content = content[:start_idx] + content[end_idx:]
        with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\utils.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Successfully removed dead block.')
    else:
        print('Could not find end index.')
else:
    print('Could not find start index.')
