import json
import numpy as np
from tkinter import Tk
import exportChoreo as exportString
import time

from pdflatex import PDFLaTeX

#3 for male plan, 11 for female plan
plan_mode=3

colors=["red","green","yellow","Apricot","white","lightgray","orange","cyan"]


name_dict = {
    "3":"1/Luis",
    "4":"2/Micha",
    "5":"3/Stephan",
    "6":"4/Tom",
    "7":"5/Simon",
    "8":"6/Tobi",
    "9":"7/Marco",
    "10":"8/Stefan",
    "11":"1/Antonia",
    "12":"2/Jan.+Ger.",
    "13":"3/Sylvie",
    "14":"4/Gina",
    "15":"5/Charlotte",
    "16":"6/Miri",
    "17":"7/Saskia",
    "18":"8/Alena",

}

coloration={key:{"idNr":(int(key)-3)%8+1,"color":colors[int(key)%8]} for key in name_dict.keys()}


def D2VecFromChoreoMaker(ChoreoMakerJSONPositionList):
    output=dict()
    for item in ChoreoMakerJSONPositionList:
        output[item["Dancer"]["$ref"]]=np.array([item["X"],item["Y"]])

    return output

def percEntageDict(distanceDict=dict()):
    total = sum(distanceDict.values())
    return {key:(value/total) for (key,value) in distanceDict.items()}

def makeMessageTikzPieChart(message1:str = "lol",message2:str = "lel",radius=3):
    out ="\\begin{tikzpicture}[baseline=(current bounding box.center)]\n"
    out+=f"\\pie[sum = auto,radius={radius},hide number,color=white]\n"
    out+=f"{{\n\t1/{{{message1}}},\n\t1/{{{message2}}}"

    return out+"\n}\n\\end{tikzpicture}"

def makeTikzPieChart(distance_dict,labeling,include_list,color,radius=3):
    out ="\\begin{tikzpicture}[baseline=(current bounding box.center)]\n"
    out+=f"\\pie[sum = auto,radius={radius},"
    out+="color={{\n\t{}\n}}]{{\n\t".format(
        ",\n\t".join([color[key]["color"] for key in distance_dict.keys() if key in include_list])
    )
    out+=",\n\t".join([f"{value:.2f}/{{{labeling[key]}}}" for (key,value) in distance_dict.items() if key in include_list])

    return out+"\n}\n\\end{tikzpicture}"

def makepage(akt,prev=None,next=None,col=coloration):
    out=f"\\begin{{center}}\n\\begin{{LARGE}}\n{akt.bild_name}"
    out+="\\\\\\noindent\\rule{\\textwidth}{1pt}\n\\end{LARGE}\end{center}\n\\begin{center}\n"
    if(next==None):
        out+=akt.lastTikzDiagram(coloring=col)

    else:
        out+=akt.tikzDiagram(next=next,coloring=col)

    out+="\\end{center}\n\\vspace{10pt}\n\\begin{center}"
    if(next==None):
        next=akt
    #Muss geändert werden
        out += akt.texTable(prev=akt)
        out+="\\scalebox{0.7}{\n"
        out += makeTikzPieChart((akt).distanceTo(),name_dict,include_list=[str(i+plan_mode) for i in range(8)],color=coloration)
    else:
    #Muss geändert werden
        out += akt.texTable(prev=next)
        out+="\\scalebox{0.7}{\n"
        out += makeTikzPieChart((next-akt).distanceTo(),name_dict,include_list=[str(i+plan_mode) for i in range(8)],color=coloration)
    out+="}\n"
    out += "\n\end{center}\n\\newpage"

    return out


def makeBlankoPage():
    out=f"\\begin{{center}}\n\\begin{{LARGE}}\n"
    out+="\\phantom{This is incredibly stupid}\\\\\\noindent\\rule{\\textwidth}{1pt}\n\\end{LARGE}\end{center}\n\\begin{center}\n"
    out+=exportString.tikzHead
    out+="\\end{tikzpicture}\n\\end{center}\n\\vspace{10pt}\n\\begin{center}\n"
    out+=exportString.tablehead+"\n"
    out+=r"\rule{0pt}{11pt} 1 &   /  &   /  &   &\multirow[t]{8}{*}{}\\ \cline{1-4}"+"\n"
    for i in range(6):
        out+= f"\\rule{{0pt}}{{11pt}} {i} &  /  &  /  & &\\\\ \\cline{{1-4}}\n"
    out+="\\rule{0pt}{11pt} 8  &   /  &   / &  &\\\\ \\hline\n\\end{tabular}"
    out+="\n"
    out += "\n\end{center}\n\\newpage"

    return out

def makeCheatSheets(scene_list,names):
    idNr="3"
    out=""
    for idNr in [str(i+3) for i in range(8)]:
        out +="\n"+ exportString.summaryTable.format(
            names[idNr],
            names[str(int(idNr)+8)],
            "\n".join([
                exportString.summaryTableIter.format(
                    scene.bild_name,
                    scene.pos_dict[idNr][0],
                    scene.pos_dict[idNr][1],
                    scene.bild_name,
                    scene.pos_dict[str(int(idNr)+8)][0],
                    scene.pos_dict[str(int(idNr)+8)][1],
                )
            for scene in scene_list]
            )
        )
    print("Hi")
    return out

def makeStatistics(scene_list,names):
    distance_list=[(scene_list[i+1]-scene_list[i]).distanceTo() for i in range(len(scene_list)-1)]
    out=""
    for idNr in [str(i+3) for i in range(16)]:
        out+=f"\\section*{{Weg Statistik von {names[idNr]}}}\n"
        out+=f"Summe: {2}"


def get_key(val,in_dict):
    for key, value in in_dict.items():
         if val == value:
             return key

    print("key doesn't exist")
    return ""

def statString(distance_dict,names):
    vals=list(distance_dict.values())
    d_sum = sum(vals)
    if(d_sum==0):
        d_sum=1
    d_max = max(vals)
    d_min = min(vals)
    d_median = np.median(vals)
    d_mean = np.mean(vals)
    d_var=np.var(vals)

    #Catch division by zero:
    divi = 1 if d_mean == 0 else d_mean

    out=f"\\makecell[lt]{{\n"
    out+=f"Max: {d_max:.1f}m ({(d_max-d_mean)*100/divi:+.0f}\\%)[{names[get_key(d_max,distance_dict)]}]\\\\ \n"
    out+=f"Min: {d_min:.2f}m ({(d_min-d_mean)*100/divi:+.0f}\\%)[{names[get_key(d_min,distance_dict)]}]\\\\ \n"
    out+=f"Med: {d_median:.2f}m\\\\ \n"
    out+=f"Mean: {d_mean:.2f}m\\\\"
    out+=f"Var: {d_var:.2f}m\\\\}}"
    return out

def makeCSV(scene_list,names):
    sorted_names_keys=[str(item) for item in sorted([int(item) for item in names.keys() ])]
    #print(sorted_names_keys)
    out=",".join([names[key] for key in sorted_names_keys])+"\n"
    out+="\n ".join([
        scene.bild_name+","+",".join(
            [str(scene.pos_dict[key][0])+","+str(scene.pos_dict[key][1]) for key in sorted_names_keys]
        )
        for scene in scene_list
    ])


    return out

def makeComplexCSV(scene_list,names):
    sorted_names_keys=[str(item) for item in sorted([int(item) for item in names.keys()])]
    #print(sorted_names_keys)
    out=",".join([names[key] for key in sorted_names_keys])+"\n"
    out+="\n".join([
        scene.bild_name+","+",".join(
            [f"{scene.pos_dict[key][0]} {scene.pos_dict[key][1]:+}i" for key in sorted_names_keys]
        )
        for scene in scene_list
    ])


    return out

class D2Dict:
    def __init__(self,pos_dict=dict()):
        self.pos_dict=pos_dict

    def __sub__(self,other):
        intersect = set(self.pos_dict.keys()).intersection(set(other.pos_dict.keys()))
        difference_dict=dict()
        for key in intersect:
            difference_dict[key]=(self.pos_dict[key][0]-other.pos_dict[key][0],self.pos_dict[key][1]-other.pos_dict[key][1])

        return D2Dict(pos_dict=difference_dict)

    #Statistics:---------------------------------------------------
    def distanceTo(self,reference=np.array([0,0])):
        output=dict()
        for key in self.pos_dict.keys():
            output[key] = np.linalg.norm(self.pos_dict[key]-reference)
        return output


class Bild(D2Dict):
    def __init__(self,pos_dict=dict(),name=""):
        super().__init__(pos_dict=pos_dict)
        self.bild_name=name

    def __len__(self):
        return len(self.pos_dict)

    def __str__(self):
        return f"{self.bild_name}:\n{self.pos_dict}"

    def __sub__(self,other):
          intersect = set(self.pos_dict.keys()).intersection(set(other.pos_dict.keys()))
          difference_dict=dict()
          for key in intersect:
              difference_dict[key]=(self.pos_dict[key][0]-other.pos_dict[key][0],self.pos_dict[key][1]-other.pos_dict[key][1])
          return Bild(pos_dict=difference_dict,name=f"Weg von {other.bild_name} nach {self.bild_name}")

    def texTable(self,prev,pairs=[(str(i+3),str(i+11)) for i in range(8)]):
        distance=(self-prev).distanceTo()
        out=exportString.tablehead
        for i in range(len(pairs)):
            out+="\n"+"\\rule{{0pt}}{{11pt}} {} &  {:.1f} / {:.1f} &  {:.1f} / {:.1f} & {:.2f}m &".format(
                i+1,
                self.pos_dict[pairs[i][0]] [0],
                self.pos_dict[pairs[i][0]] [1],
                self.pos_dict[pairs[i][1]] [0],
                self.pos_dict[pairs[i][1]] [1],
                distance[pairs[i][int((plan_mode%3)/2)]]
            )
            if i==0 and not i==len(pairs)-1:
                out+=  f"\\multirow[t]{{8}}{{*}}{{{statString(distance,name_dict)}}}"
            if i==len(pairs)-1:
                out+= "\\\\ \\hline"

            if i <len(pairs)-1:
                out+="\\\\ \\cline{1-4}"

        out+="\n\end{tabular}"
        return out

    def tikzDiagram(self,next,coloring):

        #Very Gorey Code in Latex, please dont judge
        out=exportString.tikzHead
        out+=r"\foreach \command in {"
        out+="\n\t"+r"{\draw[thin,color=green,->] (\x,\y) -- (\xn,\yn);},"
        out+="\n\t"+r"{\draw[fill=\c] (\x,\y) circle (0.4) node {\textbf{\n}};}}"+"\n{\n"

        out+=r"\foreach \n/\x/\y/\xn/\yn/\c in {"+"\n"
        out+=",\n".join(
            ["\t"+"{{{}}}/{{{}}}/{{{}}}/{{{}}}/{{{}}}/{{{}}}".format(
                coloring[key]["idNr"],
                self.pos_dict[key][0],
                self.pos_dict[key][1],
                next.pos_dict[key][0],
                next.pos_dict[key][1],
                coloring[key]["color"]
            ) for key in set(self.pos_dict.keys()).intersection(set(next.pos_dict.keys()))]
        )
        out+="}\n{\n\t\\command"
        out+="\n}\n}\n\\end{tikzpicture}"


        return out

    def lastTikzDiagram(self,coloring):

        #Very Gorey Code in Latex, please dont judge
        out=exportString.tikzHead
        out+=r"\foreach \command in {"
        out+="\n\t"+r"{\draw[fill=\c] (\x,\y) circle (0.4) node {\textbf{\n}};}}"+"\n{\n"

        out+=r"\foreach \n/\x/\y/\c in {"+"\n"
        out+=",\n".join(
            ["\t"+"{{{}}}/{{{}}}/{{{}}}/{{{}}}".format(
                coloring[key]["idNr"],
                self.pos_dict[key][0],
                self.pos_dict[key][1],
                coloring[key]["color"]
            ) for key in set(self.pos_dict.keys())]
        )
        out+="}\n{\n\t\\command"
        out+="\n}\n}\n\\end{tikzpicture}"


        return out


def makeLatexPDF(latex_string:str,tempfile_name:str ="temporaryTexFile1324532632.tex"):
    with open(tempfile_name,"w") as writer:
        writer.write(latex_string)

    pdfl = PDFLaTeX.from_texfile("E:\Privat\Tanzen\ChoreoplanTikz\Python\\"+tempfile_name)
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)


def stringToClip(output):
    print(output)
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(output)
    time.sleep(0.01)
    r.update() # now it stays on the clipboard after the window is closed
    time.sleep(0.01)
    r.destroy()

class Test:

    def test(input_int):
        exec(test+str(input_int))

    def test1():

        print(scene_positions[0])
        distances= scene_positions[0].distanceTo()
        print(list(distances.values()).index(min(distances.values())))
        print(distances)

    def test2():
        out =""
        #name_dict = {key:"$D_{{{}}}$".format(key) for key in Weg1.pos_dict.keys()}

        for key in name_dict.keys():
            name_dict[key]=f"{{{name_dict[key]}}}"

        for i in range(len(scene_positions)-1):
            out+=f"\n\\section{{Weg nach {scene_positions[i+1].bild_name}}}\n"+"\n\n\\scalebox{0.85}{"

            if(i>0):
                out+=scene_positions[i].texTable(prev=scene_positions[i-1])
            elif i==0:
                out+=scene_positions[i].texTable(prev=scene_positions[0])

            Weg1 = scene_positions[i+1]-scene_positions[i]
            #print(Weg1.pos_dict)
            distance1 = Weg1.distanceTo()
            #print(distance1)
            percentage1 = percEntageDict(distance1)

            out += makeTikzPieChart(distance1,name_dict,include_list=[str(i+plan_mode) for i in range(8)],color=coloration)
            #print(name_dict)
            out+="}"
        print(out)
        stringToClip(out)

    def test3():
        out=scene_positions[1].texTable(scene_positions[0])
        print(out)
        stringToClip(out)

    def test4():
        stringToClip(
            "\n\n".join([scene_positions[i].tikzDiagram(next=scene_positions[i+1],coloring=coloration) for i in range(len(scene_positions)-1)])
        )

    def test5():
        if(len(scene_positions)==1):
            out=makepage(akt=scene_positions[0],prev=None,next=None)+"\n\n"
        else:
            out=makepage(akt=scene_positions[0],prev=None,next=scene_positions[1])+"\n\n"
        out+="\n\n".join([
            makepage(
                akt=scene_positions[i+1],
                next=scene_positions[i+2],
                prev=scene_positions[i]
                )
            for i in range(len(scene_positions)-2)])
        if(len(scene_positions)>1):
            out+=makepage(akt=scene_positions[len(scene_positions)-1],prev=scene_positions[len(scene_positions)-2],next=None)

        out+=makeBlankoPage()
        out+=makeCheatSheets(scene_positions,names=name_dict)
        stringToClip(exportString.document_head+out+r"\end{document}")

    def test6():
        out=(makeCheatSheets(scene_positions,names=name_dict))
        stringToClip(exportString.document_head+out+r"\end{document}")

    def test7():
        print(makeStatistics(scene_positions,names=name_dict))

    def test8():
        csv_string=makeComplexCSV(scene_positions,{str(i+3):f"D{i+1}" for i in range(12)})#name_dict)
        stringToClip(csv_string)

    def test9():
        stringToClip(exportString.document_head+makeBlankoPage()+r"\end{document}")


if __name__ == "__main__":
    #print(GaussDistanz((1,0),(2,0)))
    with open("Choreo08_02.choreo") as read:
        json_choreo_text = read.read()

    choreo_dict = json.loads(json_choreo_text)

    scenes = choreo_dict["Scenes"]
    #for scene in scenes:
    #    print(D2VecFromChoreoMaker(scene["Positions"]))

    scene_positions = [Bild(D2VecFromChoreoMaker(scene["Positions"]),name=scene["Name"]) for scene in scenes]
    #for s_pos in scene_positions:
        #print(s_pos)
    scene_positions=scene_positions[0:]
    Test.test5()
    #Test.test(input("Welcher Test soll ausgeführt werden?"))
    print("Ende")
