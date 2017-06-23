# -*- coding: utf-8 -*-
#
# DCC191 A - VISUALIZACAO CIENTIFICA
# Trabalho 2 - Marching Squares
#
# Codigo implementado por: 
# Felipe Rafael
# Gilmar Ferreira
# 
# Implemetacao fortemente baseada nas ideias descritas em:
# https://en.wikipedia.org/wiki/Marching_squares
# e em exemplos disponiveis em:
# http://www.vtk.org/Wiki/VTK/Examples/Python
#

import sys,os
import vtk
from vtk.util import numpy_support as VN


def view(points, lines):

	# Create a polydata to store everything in
	linesPolyData = vtk.vtkPolyData()
	 
	# Add the points to the dataset
	linesPolyData.SetPoints(points)
	 
	# Add the lines to the dataset
	linesPolyData.SetLines(lines)
	 
	# Setup actor and mapper
	mapper = vtk.vtkPolyDataMapper()
	if vtk.VTK_MAJOR_VERSION <= 5:
	    mapper.SetInput(linesPolyData)
	else:
	    mapper.SetInputData(linesPolyData)
	 
	actor = vtk.vtkActor()
	actor.SetMapper(mapper)
	 
	# Setup render window, renderer, and interactor
	renderer = vtk.vtkRenderer()
	renderer.SetBackground(0.25, 0.25, 0.25)
	renderer.AddActor(actor)
	renderWindow = vtk.vtkRenderWindow()
	renderWindow.AddRenderer(renderer)
	renderWindowInteractor = vtk.vtkRenderWindowInteractor()
	renderWindowInteractor.SetRenderWindow(renderWindow)
	
	 
	renderWindow.Render()
	renderWindowInteractor.Start()

# end_of_view

def interpolate(pi, pj, axis, cell_pts, scalar, val):

	a = cell_pts.GetPoint(pi)[axis] * (scalar[pj] - val)
	b = cell_pts.GetPoint(pj)[axis] * (val - scalar[pi])
	c = scalar[pj] - scalar[pi]

	return (a + b) / c

# end_of_interpolate

def contour(input_file):

	# Leitura do arquivo
	reader = vtk.vtkUnstructuredGridReader()
	reader.SetFileName(input_file)
	reader.Update()

	# objeto que "guarda" a malha
	output_grid  = reader.GetOutput()
	# intervalo de valores dos escalares
	scalar_range = output_grid.GetScalarRange()
	# dados associados aos pontos
	point_data   =  output_grid.GetPointData()
	# escalares associados aos dados dos pontos
	point_scalars = point_data.GetScalars()

	# obtem o escalar, para o contorno, do usuário
	try:
		print '\nInforme o escalar (deve estar no intervalo [%.2f,%.2f]): ' % (scalar_range[0],scalar_range[1])
		val = float(raw_input())
	except ValueError:
		print "Nao e um numero... =(\n"
		sys.exit(-1)
	if val < scalar_range[0] or val > scalar_range[1]:
		print "Escalar fora do intervalo valido... =("
		sys.exit(-1)

	isoline_points = vtk.vtkPoints()
	lines          = vtk.vtkCellArray()

	# itera em cada célula
	num_cells = output_grid.GetNumberOfCells()
	for i in range(num_cells):
		cell     = output_grid.GetCell(i)
		cell_pts = cell.GetPoints()

		# variável que mapeia o indice de uma célula baseando-se em uma lookup table
		# que considera um vértice de uma célula igual a 1 se seu escalar é maior
		# que o escalar da isolinha e igual a 0 caso contrário
		cell_index = 0
		# ponto de uma celula e escalares associados a cada ponto de uma celula
		point  = [None] * 3
		scalar = [None] * 4

		#itera em cada ponto da célula
		num_points = cell_pts.GetNumberOfPoints()
		for j in range(num_points):
			scalar[j] = point_scalars.GetTuple1(cell.GetPointId(j))
			if scalar[j] < val:
				if j == 2:
					p = 3
				elif j == 3:
					p = 2
				else:
					p = j

				cell_index += 2**p # valor obtido já convertido para decimal

		# se cell_index == 0 ou cell_index == 15:
		# não faz nada já que a celula está totalmente acima
		# ou totalmente abaixo da isolinha
		if cell_index == 1 or cell_index == 14:
			for k in range(3):
				point[k] = (interpolate(0, 1, k, cell_pts, scalar, val))
			a = isoline_points.InsertNextPoint(point)

			for k in range(3):
				point[k] = (interpolate(0, 2, k, cell_pts, scalar, val))
			b = isoline_points.InsertNextPoint(point)

			line = vtk.vtkLine()
			line.GetPointIds().SetId(0, a)
			line.GetPointIds().SetId(1, b)

			lines.InsertNextCell(line)
		elif cell_index == 2 or cell_index == 13:
			for k in range(3):
				point[k] = (interpolate(0, 1, k, cell_pts, scalar, val))
			a = isoline_points.InsertNextPoint(point)

			for k in range(3):
				point[k] = (interpolate(1, 3, k, cell_pts, scalar, val))
			b = isoline_points.InsertNextPoint(point)

			line = vtk.vtkLine()
			line.GetPointIds().SetId(0, a)
			line.GetPointIds().SetId(1, b)

			lines.InsertNextCell(line)
		elif cell_index == 3 or cell_index == 12:
			for k in range(3):
				point[k] = (interpolate(0, 2, k, cell_pts, scalar, val))
			a = isoline_points.InsertNextPoint(point)

			for k in range(3):
				point[k] = (interpolate(1, 3, k, cell_pts, scalar, val))
			b = isoline_points.InsertNextPoint(point)

			line = vtk.vtkLine()
			line.GetPointIds().SetId(0, a)
			line.GetPointIds().SetId(1, b)

			lines.InsertNextCell(line)
		elif cell_index == 4 or cell_index == 11:
			for k in range(3):
				point[k] = (interpolate(1, 3, k, cell_pts, scalar, val))
			a = isoline_points.InsertNextPoint(point)

			for k in range(3):
				point[k] = (interpolate(2, 3, k, cell_pts, scalar, val))
			b = isoline_points.InsertNextPoint(point)

			line = vtk.vtkLine()
			line.GetPointIds().SetId(0, a)
			line.GetPointIds().SetId(1, b)

			lines.InsertNextCell(line)
		elif cell_index == 5 or cell_index == 10:
			for k in range(3):
				point[k] = (interpolate(0, 1, k, cell_pts, scalar, val))
			a = isoline_points.InsertNextPoint(point)

			for k in range(3):
				point[k] = (interpolate(1, 3, k, cell_pts, scalar, val))
			b = isoline_points.InsertNextPoint(point)

			for k in range(3):
				point[k] = (interpolate(2, 3, k, cell_pts, scalar, val))
			c = isoline_points.InsertNextPoint(point)

			for k in range(3):
				point[k] = (interpolate(0, 2, k, cell_pts, scalar, val))
			d = isoline_points.InsertNextPoint(point)

			# trata caso ambiguo verificando a media dos quatro escalares
			mean = 0.0
			for k in range(3):
				mean += scalar[k]
			mean /= 4
			if (mean < val) == (scalar[0] < val):
				line = vtk.vtkLine()
				line.GetPointIds().SetId(0, a)
				line.GetPointIds().SetId(1, b)

				lines.InsertNextCell(line)

				line = vtk.vtkLine()
				line.GetPointIds().SetId(0, c)
				line.GetPointIds().SetId(1, d)

				lines.InsertNextCell(line)
			else:
				line = vtk.vtkLine()
				line.GetPointIds().SetId(0, a)
				line.GetPointIds().SetId(1, d)

				lines.InsertNextCell(line)

				line = vtk.vtkLine()
				line.GetPointIds().SetId(0, b)
				line.GetPointIds().SetId(1, c)

				lines.InsertNextCell(line)
		elif cell_index == 6 or cell_index == 9:
			for k in range(3):
				point[k] = (interpolate(2, 3, k, cell_pts, scalar, val))
			a = isoline_points.InsertNextPoint(point)

			for k in range(3):
				point[k] = (interpolate(0, 1, k, cell_pts, scalar, val))
			b = isoline_points.InsertNextPoint(point)

			line = vtk.vtkLine()
			line.GetPointIds().SetId(0, a)
			line.GetPointIds().SetId(1, b)

			lines.InsertNextCell(line)
		elif cell_index == 7 or cell_index == 8:
			for k in range(3):
				point[k] = (interpolate(0, 2, k, cell_pts, scalar, val))
			a = isoline_points.InsertNextPoint(point)

			for k in range(3):
				point[k] = (interpolate(2, 3, k, cell_pts, scalar, val))
			b = isoline_points.InsertNextPoint(point)

			line = vtk.vtkLine()
			line.GetPointIds().SetId(0, a)
			line.GetPointIds().SetId(1, b)

			lines.InsertNextCell(line)
		elif cell_index != 0 and cell_index != 15:
			print "\n Algo errado nao esta certo... =(\n"
			sys.exit(-1)

	# chama a rotina para visualização do contorno
	view(isoline_points, lines)

# end_of_contour

if __name__ == "__main__":

	if(len(sys.argv) != 2):
		print("\nUsage: python main.py <file.vtk>\n")
		sys.exit(-1)

	input_file = sys.argv[1]
	if(not os.path.isfile(input_file)):
		print("\nError: Input %s does not exist.\n" % (input_file))
		sys.exit(-1)

	# chama a função que implementa o Marching Squares
	contour(input_file)

# end_of_main
