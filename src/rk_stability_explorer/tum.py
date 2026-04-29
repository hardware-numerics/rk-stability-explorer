#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:28:49 2026

@author: gransalis
"""

import numpy as np
import math

class Particle:
    def __init__(self, mass, pos, vel, spin=1):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.spin = spin



def rotate(vec, euler):
    theta, psi, phi = np.radians(euler)
    
    c1, c2, c3 = np.cos([theta, psi, phi])
    s1, s2, s3 = np.sin([theta, psi, phi])
    
    R = np.array([
        [c2*c3 - c1*s2*s3,  -c2*s3 - c1*s2*c3,  s1*s2],
        [s2*c3 + c1*c2*s3,  -s2*s3 + c1*c2*c3, -s1*c2],
        [s1*s3,              s1*c3,             c1]
    ])
    
    return R @ vec

def circ_vel(r, M):
    return np.sqrt(M / r)   # G = 1


def set_ICs(
    mass1=1.0,
    mass2=1.0,
    pos1=[-1.5, -1.5, 0],
    pos2=[1.5, 1.5, 0],
    vel1=[0, 0.3, 0],
    vel2=[0, -0.3, 0],
    euler1=[0, 0, 0],
    euler2=[0, 0, 0],
    spin1=1,
    spin2=1,
    n_rings=5,
    stars_per_ring=50,
    ring_spacing=0.2
):
    # --- halos ---
    halo1 = Particle(mass1, pos1, vel1, spin1)
    halo2 = Particle(mass2, pos2, vel2, spin2)
    halos = [halo1, halo2]
    
    stars = []
    
    for i, halo in enumerate(halos):
        galaxy_stars = []
        euler = euler1 if i == 0 else euler2
        
        for ring in range(n_rings):
            r = ring_spacing * (ring + 1)
            
            for k in range(stars_per_ring):
                angle = 2 * np.pi * k / stars_per_ring
                
                # position in disk
                local_pos = np.array([
                    np.cos(angle),
                    np.sin(angle),
                    0
                ]) * r
                
                pos = rotate(local_pos, euler) + halo.pos
                
                # circular velocity
                v = circ_vel(r, halo.mass)
                
                local_vel = np.array([
                    -np.sin(angle),
                    np.cos(angle),
                    0
                ]) * v * halo.spin
                
                vel = rotate(local_vel, euler) + halo.vel
                
                galaxy_stars.append(
                    Particle(0.0, pos, vel)  # test particles
                )
        
        stars.append(galaxy_stars)
    
    return halos, stars

def particles_to_arrays(halos, stars):
    all_particles = []
    
    # halos first (important!)
    all_particles.extend(halos)
    
    # then stars
    for galaxy in stars:
        all_particles.extend(galaxy)
    
    N = len(all_particles)
    
    positions = np.zeros((N, 3))
    velocities = np.zeros((N, 3))
    masses = np.zeros(N)
    
    for i, p in enumerate(all_particles):
        positions[i] = p.pos
        velocities[i] = p.vel
        masses[i] = p.mass
    
    return positions, velocities, masses
    
def compute_accelerations(positions, masses, eps=1e-3):
    """
    Compute accelerations in normalized units (G = 1).
    
    positions: (N, d)
    masses: (N,)
    eps: softening parameter
    """
    N = len(masses)
    acc = np.zeros_like(positions)
    
    for i in range(N):
        diff = positions[i] - positions
        dist2 = np.sum(diff**2, axis=1) + eps**2
        inv_dist3 = dist2**(-1.5)
        
        inv_dist3[i] = 0.0  # remove self-interaction
        
        acc[i] = -np.sum((masses[:, None] * diff) * inv_dist3[:, None], axis=0)
    
    return acc

def compute_energy_halo(positions, velocities, masses):
    # предполагаем: первые 2 частицы — гало
    p = positions[:2]
    v = velocities[:2]
    m = masses[:2]
    
    kinetic = 0.5 * np.sum(m * np.sum(v**2, axis=1))
    
    r = np.linalg.norm(p[0] - p[1])
    potential = - m[0] * m[1] / r
    
    return kinetic + potential

def compute_accelerations_restricted(positions, masses, eps=1e-3):
    # assume first 2 particles = halos
    halos_pos = positions[:2]
    halos_mass = masses[:2]
    
    N = len(positions)
    acc = np.zeros_like(positions)
    
    # halo-halo interaction (2-body)
    for i in range(2):
        for j in range(2):
            if i == j:
                continue
            dx = positions[i] - positions[j]
            r2 = np.sum(dx**2) + eps**2
            acc[i] -= halos_mass[j] * dx / (r2 * np.sqrt(r2))
    
    # stars feel halos only
    for i in range(2, N):
        for j in range(2):
            dx = positions[i] - halos_pos[j]
            r2 = np.sum(dx**2) + eps**2
            acc[i] -= halos_mass[j] * dx / (r2 * np.sqrt(r2))
    
    return acc

def rk4_step(positions, velocities, masses, dt, acc_fn):
    def acceleration(pos):
        return acc_fn(pos, masses)
    
    k1_v = acceleration(positions)
    k1_x = velocities
    
    k2_v = acceleration(positions + 0.5 * dt * k1_x)
    k2_x = velocities + 0.5 * dt * k1_v
    
    k3_v = acceleration(positions + 0.5 * dt * k2_x)
    k3_x = velocities + 0.5 * dt * k2_v
    
    k4_v = acceleration(positions + dt * k3_x)
    k4_x = velocities + dt * k3_v
    
    new_positions = positions + (dt / 6.0) * (k1_x + 2*k2_x + 2*k3_x + k4_x)
    new_velocities = velocities + (dt / 6.0) * (k1_v + 2*k2_v + 2*k3_v + k4_v)
    
    return new_positions, new_velocities

def verlet_step(positions, velocities, masses, dt, acc_fn):
    acc = acc_fn(positions, masses)
    
    # half-step velocity
    v_half = velocities + 0.5 * dt * acc
    
    # full-step position
    new_positions = positions + dt * v_half
    
    # new acceleration
    new_acc = acc_fn(new_positions, masses)
    
    # complete velocity step
    new_velocities = v_half + 0.5 * dt * new_acc
    
    return new_positions, new_velocities

def euler_step(positions, velocities, masses, dt, acc_fn):
    acc = acc_fn(positions, masses)
    
    new_positions = positions + dt * velocities
    new_velocities = velocities + dt * acc
    
    return new_positions, new_velocities

def simulate(positions, velocities, masses, dt, steps, method, acc_fn, energy_fn=None):
    traj = []
    energies = []
    
    pos = positions.copy()
    vel = velocities.copy()
    
    for _ in range(steps):
        traj.append(pos.copy())
        
        if energy_fn is not None:
            energies.append(energy_fn(pos, vel, masses))
        
        pos, vel = step(method, pos, vel, masses, dt, acc_fn)
    
    return np.array(traj), np.array(energies)
    
def compute_energy(positions, velocities, masses):
    """
    Total energy in normalized units.
    """
    kinetic = 0.5 * np.sum(masses * np.sum(velocities**2, axis=1))
    
    potential = 0.0
    N = len(masses)
    for i in range(N):
        for j in range(i+1, N):
            r = np.linalg.norm(positions[i] - positions[j])
            potential -= masses[i] * masses[j] / r
    
    return kinetic + potential

def step(method, positions, velocities, masses, dt, acc_fn):
    return method(positions, velocities, masses, dt, acc_fn)


halos, stars = set_ICs()

positions, velocities, masses = particles_to_arrays(halos, stars)

traj, energy = simulate(
    positions,
    velocities,
    masses,
    dt=0.01,
    steps=100,
    method=euler_step,   # method is defined here
    #method=rk4_step,   # method is defined here
    #method=verlet_step,   # method is defined here
    acc_fn=compute_accelerations_restricted,
    energy_fn=compute_energy_halo
)