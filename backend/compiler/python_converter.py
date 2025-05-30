# -----------------------
# STAGE 4: Python Generator
# -----------------------
import re

def generate_python(ir, indent=0):
    lines = []
    indent_str = '    ' * indent

    for instr in ir:
        if instr['op'] == 'assign':
            lines.append(f"{indent_str}{instr['target']} = {instr['value']}")

        elif instr['op'] == 'print':
            lines.append(f"{indent_str}print({instr['value']})")

        elif instr['op'] == 'function_def':
            lines.append(f"{indent_str}def {instr['name']}({', '.join(instr['params'])}):")
            body = generate_python(instr['body'], indent + 1)
            lines.append(body if body else f"{indent_str}    pass")

        elif instr['op'] == 'if_chain':
            for idx, branch in enumerate(instr['branches']):
                keyword = branch['type']
                cond = branch.get('condition', '')
                prefix = 'if' if idx == 0 else 'elif' if keyword == 'elif' else 'else'
                condition_str = f" {cond}:" if prefix != 'else' else ':'
                lines.append(f"{indent_str}{prefix}{condition_str}")
                body = generate_python(branch['body'], indent + 1)
                lines.append(body if body else f"{indent_str}    pass")

        elif instr['op'] == 'while':
            lines.append(f"{indent_str}while {instr['condition']}:")
            body = generate_python(instr['body'], indent + 1)
            lines.append(body if body else f"{indent_str}    pass")

        elif instr['op'] == 'do_while':
            lines.append(f"{indent_str}while True:")
            body = generate_python(instr['body'], indent + 1)
            lines.append(body if body else f"{indent_str}    pass")
            lines.append(f"{indent_str}    if not ({instr['condition']}):")
            lines.append(f"{indent_str}        break")

        elif instr['op'] == 'for_loop':
            # Parse for loop components
            init = instr['init']         # e.g. "i = 1"
            cond = instr['condition']    # e.g. "i <= 5"
            incr = instr['increment']    # e.g. "i++" or "i--"

            try:
                var = init.split('=')[0].strip()
                start = int(init.split('=')[1].strip())

                # Match condition like: i <= 5, i < 6, i >= 1, i > 0
                m = re.match(rf"{var}\s*([<>]=?)\s*(-?\d+)", cond)
                if m:
                    op, end_val_str = m.group(1), m.group(2)
                    end_val = int(end_val_str)

                    # Determine step from increment
                    step = 1
                    if incr.strip() in (f"{var}++", f"{var} += 1"):
                        step = 1
                    elif incr.strip() in (f"{var}--", f"{var} -= 1"):
                        step = -1
                    else:
                        step = 1  # fallback

                    # Calculate Python range end based on operator and step
                    if step > 0:
                        # Increasing loop
                        if op == '<=':
                            range_end = end_val + 1
                        elif op == '<':
                            range_end = end_val
                        else:
                            range_end = end_val + 1  # fallback
                    else:
                        # Decreasing loop
                        if op == '>=':
                            range_end = end_val - 1
                        elif op == '>':
                            range_end = end_val
                        else:
                            range_end = end_val - 1  # fallback

                    step_str = f", {step}" if step != 1 else ""

                    lines.append(f"{indent_str}for {var} in range({start}, {range_end}{step_str}):")
                    body = generate_python(instr['body'], indent + 1)
                    lines.append(body if body else f"{indent_str}    pass")
                    continue  # done with for loop

            except Exception:
                pass  # fallback to while loop if parsing fails

            # Fallback to while loop style
            lines.append(f"{indent_str}{init}")
            lines.append(f"{indent_str}while {cond}:")
            body = generate_python(instr['body'], indent + 1)
            lines.append(body if body else f"{indent_str}    pass")
            lines.append(f"{indent_str}    {incr}")
        elif instr['op'] == 'update':
            if instr['operator'] == '++':
                lines.append(f"{indent_str}{instr['target']} += 1")
            elif instr['operator'] == '--':
                lines.append(f"{indent_str}{instr['target']} -= 1")

        elif instr['op'] == 'return':
            lines.append(f"{indent_str}return {instr['value']}")

    return "\n".join(lines)
