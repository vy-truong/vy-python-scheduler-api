from ortools.sat.python import cp_model

def create_shift_scheduling_model(
    num_employees, shifts_per_day, total_days, employee_types, full_time_hours=40, part_time_hours=20, full_shift=8, half_shift=4
):
    model = cp_model.CpModel()

    all_employees = range(num_employees)
    all_shifts = range(shifts_per_day)
    all_days = range(total_days)

    shifts = {}
    for employee in all_employees:
        for day in all_days:
            for shift in all_shifts:
                shifts[(employee, day, shift)] = model.NewBoolVar(f"shift_e{employee}_d{day}_s{shift}")

    for employee in all_employees:
        for day in all_days:
            model.AddAtMostOne(shifts[(employee, day, shift)] for shift in all_shifts)

    for day in all_days:
        for shift in all_shifts:
            model.AddExactlyOne(shifts[(employee, day, shift)] for employee in all_employees)

    for employee in all_employees:
        if employee_types[employee] == 'part_time':
            total_hours = sum(shifts[(employee, day, shift)] * half_shift for day in all_days for shift in all_shifts)
            model.Add(total_hours <= part_time_hours)
        elif employee_types[employee] == 'full_time':
            total_hours = sum(shifts[(employee, day, shift)] * full_shift for day in all_days for shift in all_shifts)
            model.Add(total_hours <= full_time_hours)

    for employee in all_employees:
        if employee_types[employee] == 'full_time':
            total_shifts_worked = sum(shifts[(employee, day, shift)] for day in all_days for shift in all_shifts)
            model.Add(total_shifts_worked >= 1)

    return model, shifts

def solve_shift_scheduling(model, shifts, num_employees, shifts_per_day, total_days, solution_limit=5):
    solver = cp_model.CpSolver()

    class SolutionPrinter(cp_model.CpSolverSolutionCallback):
        def __init__(self, shifts, num_employees, shifts_per_day, total_days, limit=5):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._shifts = shifts
            self._num_employees = num_employees
            self._shifts_per_day = shifts_per_day
            self._total_days = total_days
            self._solution_count = 0
            self._solution_limit = limit
            self._results = []

        def on_solution_callback(self):
            self._solution_count += 1
            result = {}
            for day in range(self._total_days):
                day_result = []
                for shift in range(self._shifts_per_day):
                    for employee in range(self._num_employees):
                        if self.Value(self._shifts[(employee, day, shift)]):
                            day_result.append({"employee": employee, "shift": shift})
                result[f"Day {day + 1}"] = day_result
            self._results.append(result)
            if self._solution_count >= self._solution_limit:
                self.StopSearch()

        def get_results(self):
            return self._results

    solution_printer = SolutionPrinter(shifts, num_employees, shifts_per_day, total_days, solution_limit)
    solver.SolveWithSolutionCallback(model, solution_printer)
    return solution_printer.get_results()
