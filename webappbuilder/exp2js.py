#===============================================================================
# This code belong to the gis2js library, by Nathan Woodrow
# https://github.com/NathanW2/qgs2js
#===============================================================================

from qgis.core import QgsExpression
import re, json
import os

whenfunctions = []

binary_ops = [
    "||", "&&",
    "==", "!=", "<=", ">=", "<", ">", "~",
    "LIKE", "NOT LIKE", "ILIKE", "NOT ILIKE", "===", "!==",
    "+", "-", "*", "/", "//", "%", "^",
    "+"
]

unary_ops = ["!", "-"]


def compile(expstr, name=None, mapLib=None):
    """
    Convert a QgsExpression into a JS function.
    """
    return exp2func(expstr, name, mapLib)


def exp2func(expstr, name=None, mapLib=None):
    """
    Convert a QgsExpression into a JS function.
    """
    global whenfunctions
    whenfunctions = []
    exp = QgsExpression(expstr)
    if expstr:
        js = walkExpression(exp.rootNode(), mapLib=mapLib)
    else:
        js = "true"
    if name is None:
        import random
        import string
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
    name += "_eval_expression"
    temp = """
function %s(context) {
    // %s

    var feature = context.feature;
    %s
    return %s;
}""" % (name,
        exp.dump(),
        "\n".join(whenfunctions),
        js)
    return temp, name, exp.dump()



def walkExpression(node, mapLib):
    if node.nodeType() == QgsExpression.ntBinaryOperator:
        jsExp = handle_binary(node, mapLib)
    elif node.nodeType() == QgsExpression.ntUnaryOperator:
        jsExp = handle_unary(node, mapLib)
    elif node.nodeType() == QgsExpression.ntInOperator:
        jsExp = handle_in(node, mapLib)
    elif node.nodeType() == QgsExpression.ntFunction:
        jsExp = handle_function(node, mapLib)
    elif node.nodeType() == QgsExpression.ntLiteral:
        jsExp = handle_literal(node)
    elif node.nodeType() == QgsExpression.ntColumnRef:
        jsExp = handle_columnRef(node, mapLib)
    elif node.nodeType() == QgsExpression.ntCondition:
        jsExp = handle_condition(node,mapLib)
    return jsExp


def handle_condition(node, mapLib):
    global condtioncounts
    subexps = re.findall("WHEN(\s+.*?\s+)THEN(\s+.*?\s+)", node.dump())
    count = 1;
    js = ""
    for sub in subexps:
        when = sub[0].strip()
        then = sub[1].strip()
        whenpart =  QgsExpression(when)
        thenpart = QgsExpression(then)
        whenjs = walkExpression(whenpart.rootNode(), mapLib)
        thenjs = "null" if thenpart.rootNode() is None else walkExpression(thenpart.rootNode(), mapLib)
        style = "if" if count == 1 else "else if"
        js += """
        %s %s {
          return %s;
        }
        """ % (style, whenjs, thenjs)
        js = js.strip()
        count += 1

    elsejs = "null"
    if "ELSE" in node.dump():
        elseexps = re.findall("ELSE(\s+.*?\s+)END", node.dump())
        elsestr = elseexps[0].strip()
        exp =  QgsExpression(elsestr)
        elsejs = walkExpression(exp.rootNode(), mapLib)
    funcname = "_CASE()"
    temp = """function %s {
    %s
    else {
     return %s;
    }
    };""" % (funcname, js, elsejs)
    whenfunctions.append(temp)
    return funcname

def handle_binary(node, mapLib):
    op = node.op()
    retOp = binary_ops[op]
    left = node.opLeft()
    right = node.opRight()
    retLeft = walkExpression(left, mapLib)
    retRight = walkExpression(right, mapLib)
    if retOp == "LIKE":
        return "(%s.indexOf(%s) > -1)" % (retLeft[:-1],
                                          re.sub("[_%]", "", retRight))
    elif retOp == "NOT LIKE":
        return "(%s.indexOf(%s) == -1)" % (retLeft[:-1],
                                           re.sub("[_%]", "", retRight))
    elif retOp == "ILIKE":
        return "(%s.toLowerCase().indexOf(%s.toLowerCase()) > -1)" % (
            retLeft[:-1],
            re.sub("[_%]", "", retRight))
    elif retOp == "NOT ILIKE":
        return "(%s.toLowerCase().indexOf(%s.toLowerCase()) == -1)" % (
            retLeft[:-1],
            re.sub("[_%]", "", retRight))
    elif retOp == "~":
        return "/%s/.test(%s)" % (retRight[1:-2], retLeft[:-1])
    elif retOp == "//":
        return "(Math.floor(%s %s %s))" % (retLeft, retOp, retRight)
    else:
        return "(%s %s %s)" % (retLeft, retOp, retRight)


def handle_unary(node, mapLib):
    op = node.op()
    operand = node.operand()
    retOp = unary_ops[op]
    retOperand = walkExpression(operand, mapLib)
    return "%s %s " % (retOp, retOperand)


def handle_in(node, mapLib):
    operand = node.node()
    retOperand = walkExpression(operand, mapLib)
    list = node.list().dump()
    retList = json.dumps(list)
    return "%s.indexOf(%s) > -1 " % (retList, retOperand)


def handle_literal(node):
    val = node.value()
    quote = ""
    if isinstance(val, basestring):
        quote = "'"
        val = val.replace("\n", "\\n")
    elif val is None:
        val = "null"

    return "%s%s%s" % (quote, unicode(val), quote)


def handle_function(node, mapLib):
    fnIndex = node.fnIndex()
    func = QgsExpression.Functions()[fnIndex]
    retArgs = []
    retFunc = (func.name().replace("$", "_"))
    args = node.args()
    if args is not None:
        args = args.list()
        for arg in args:
            retArgs.append(walkExpression(arg, mapLib))
        retArgs = ",".join(retArgs)
    return "fnc_%s([%s], context)" % (retFunc, retArgs)


def handle_columnRef(node, mapLib):
    return "feature.get('%s') " % node.name()

def compile_to_file(exp, name=None, mapLib=None, filename="expressions.js"):
    """
    Generate JS function to file from exp and append it to the end of the given file name.
    :param exp: The expression to export to JS
    :return: The name of the function you can call.
    """
    functionjs, name, _ = compile(exp, name=name, mapLib=mapLib)
    with open(filename, "a") as f:
        f.write("\n\n")
        f.write(functionjs)

    return name


def is_expression_supported(expr):
    path = os.path.join(os.path.dirname(__file__), "js", "qgis2web_expressions.js")
    with open(path) as f:
        lines = f.readlines()
    used = [str(e) for e in re.findall("[a-zA-Z]{2,}?\(", expr)]
    print used
    unsupported = []
    for i, line in enumerate(lines):
        for func in used:
            if func in line:
                if "return false" in lines[i + 1]:
                    unsupported.append(func[:-1])
                break

    return unsupported



