class Rocket:
    def __init__(self,dry_mass, fuel_mass, diameter, Cd, thrust, burn_time):
        self.dry_mass = dry_mass
        self.fuel_mass = fuel_mass
        self.diameter = diameter
        self.Cd = Cd
        self.thrust = thrust
        self.burn_time = burn_time
        self.mass_flow_rate = fuel_mass / burn_time

    def get_mass(self):
        return self.dry_mass + self.fuel_mass 

    def get_area(self):
        return 3.14159 * (self.diameter)**2 / 4
    
    def get_thrust(self, time):
        if time < self.burn_time:
            return self.thrust
        else:
            return 0

    def consume_fuel(self, dt):
        fuel_to_burn = self.mass_flow_rate * dt

        if fuel_to_burn <= self.fuel_mass:
            self.fuel_mass -= fuel_to_burn
            return fuel_to_burn
        else:
            fuel_consumed = self.fuel_mass
            self.fuel_mass = 0
            return fuel_consumed

class Environment:
    def __init__(self):
        self.gravity = 9.81
        self.air_density = 1.225

    def get_gravity(self):
        return self.gravity

    def get_air_density(self):
        return self.air_density


class Simulation:
    def __init__(self,rocket,environment,dt):
        self.rocket = rocket
        self.environment = environment
        self.dt = dt
        self.time = 0
        self.altitude = 0
        self.velocity = 0
        self.acceleration = 0

    def get_state(self):
        state = self.__dict__.copy()
        state["mass"] = self.rocket.get_mass()
        state.pop('rocket', None)
        state.pop('environment', None) 
        state.pop("yakit", None)
        return state

    def calculate_drag(self):
        air_density = self.environment.get_air_density()
        area = self.rocket.get_area()
        drag = 0.5 * air_density * self.velocity**2 * self.rocket.Cd * area
        if self.velocity > 0:
            return -drag
        elif self.velocity < 0:
            return drag
        else:
            return 0

    def calculate_net_force(self):
        thrust = self.rocket.get_thrust(self.time)
        drag = self.calculate_drag()
        gravity_force = self.rocket.get_mass() * self.environment.get_gravity()
        fnet = thrust + drag - gravity_force
        return fnet

    def calculate_acceleration(self):
        fnet= self.calculate_net_force()
        mass = self.rocket.get_mass()
        return fnet/mass

    def update(self):
        self.acceleration=self.calculate_acceleration()
        self.velocity += self.acceleration * self.dt 
        self.altitude += self.velocity * self.dt
        if self.altitude <0:
            self.altitude=0
            self.velocity=0
        self.yakit = self.rocket.consume_fuel(self.dt)
        self.time += self.dt 

    def run(self, max_time):
        time_history = []
        altitude_history = []
        velocity_history = []
        acceleration_history = []
        while self.time < max_time and self.altitude >= 0:
            self.update()
            
            time_history.append(self.time)
            altitude_history.append(self.altitude)
            velocity_history.append(self.velocity)
            acceleration_history.append(self.acceleration)

            state=self.get_state()
            state["mass"]= self.rocket.dry_mass + self.rocket.fuel_mass
            if self.time > self.dt and self.altitude==0:
                break
            else:
                print(state)
                print(self.time, self.rocket.fuel_mass, self.rocket.get_mass())

        self.a = max(altitude_history)
        yuksek = altitude_history.index(self.a)
        self.t_a = time_history[yuksek]

        self.v= max(velocity_history)
        hizli = velocity_history.index(self.v)
        self.t_v = time_history[hizli]

        self.acce= max(acceleration_history)
        ivme = acceleration_history.index(self.acce)
        self.t_acce = time_history[ivme]

        self.son=time_history[-1]



rocket = Rocket(15,5,0.1,0.45,1200,5)
environment = Environment()

simulation = Simulation(rocket, environment, 0.1)

simulation.run(100)


print("------------------")
print("SIMULATION RESULTS")
print("------------------")
print("Max altitude: ", simulation.a)
print("Time of maximum altitude: ", simulation.t_a)
print("Max velocity: ", simulation.v)
print("Time of maximum velocity: ", simulation.t_v)
print("Fuel remaining: ", simulation.rocket.fuel_mass)
print("Total flight time: ", simulation.son)
print("Maximum acceleration: ", simulation.acce)
print("Time of maximum acceleration: ", simulation.t_acce)
