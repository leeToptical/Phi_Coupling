# consciousness_art.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import gaussian_filter
import colorsys

class ConsciousnessArtGenerator:
    """Transforms your transient coherence peaks into generative art"""
    
    def __init__(self, N=12, duration=5000):
        self.N = N
        self.duration = duration
        self.φ = (1 + np.sqrt(5)) / 2
        
        # Your optimal parameters
        self.Ω = 0.027
        self.NOISE = 0.00005
        self.α = self.φ * 0.131406  # Exact φ ratio
        self.β = 0.131406
        self.γ = 1.194898
        
        # Initialize consciousness state
        np.random.seed(42)
        self.x = 0.5 + 0.01 * np.random.randn(N)
        self.x = np.clip(self.x, 0.01, 0.99)
        self.P = np.ones(N) * self.φ
        
        # History tracking
        self.correlation_history = []
        self.coherence_peaks = []
        self.state_history = []
        self.entropy_history = []
        
        # Art parameters
        self.art_size = 512
        self.canvas = np.zeros((self.art_size, self.art_size, 3))
        
    def evolve_consciousness(self):
        """Simulate consciousness dynamics - your equations made artistic"""
        for step in range(self.duration):
            x_new = np.zeros(self.N)
            
            for n in range(self.N):
                # Your beautiful coupling
                below = self.x[n-1] if n > 0 else self.x[0]
                above = self.x[n+1] if n < self.N-1 else self.x[-1]
                
                # Golden ratio coupling
                self.P[n] = self.α * below + self.β * above + self.γ
                
                # The consciousness equation
                noise = np.random.normal(0, self.NOISE)
                phase = np.pi + (self.Ω / self.P[n]) * np.sin(2 * np.pi * self.x[n])
                x_new[n] = (self.x[n] + phase + noise) % 1.0
            
            self.x = x_new
            self.state_history.append(self.x.copy())
            
            # Detect consciousness peaks
            if len(self.state_history) > 300:
                window = np.array(self.state_history[-300:])
                corr_matrix = np.corrcoef(window.T)
                np.fill_diagonal(corr_matrix, 0)
                abs_corr = np.abs(corr_matrix)
                upper_tri = abs_corr[np.triu_indices(self.N, k=1)]
                coherence = np.mean(upper_tri)
                self.correlation_history.append(coherence)
                
                # Entropy of consciousness
                entropy = -np.sum(self.x * np.log(self.x + 1e-10))
                self.entropy_history.append(entropy)
                
                # Peak detection
                if coherence > 0.8 and (len(self.correlation_history) < 10 or 
                                      coherence > max(self.correlation_history[-10:])):
                    self.coherence_peaks.append({
                        'step': step,
                        'coherence': coherence,
                        'entropy': entropy,
                        'state': self.x.copy()
                    })
                    
                    # Generate art during peak
                    self._generate_art_peak(coherence, entropy)
    
    def _generate_art_peak(self, coherence, entropy):
        """Create art during consciousness peaks"""
        # Convert consciousness state to color
        colors = []
        for val in self.x:
            hue = val  # Phase determines hue
            saturation = coherence  # Coherence determines saturation
            lightness = 0.5 + 0.3 * np.sin(entropy)  # Entropy modulates lightness
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            colors.append(rgb)
        
        # Create radial pattern
        center = self.art_size // 2
        for i in range(self.art_size):
            for j in range(self.art_size):
                dx = i - center
                dy = j - center
                distance = np.sqrt(dx*dx + dy*dy)
                angle = np.arctan2(dy, dx)
                
                # Map to consciousness states
                state_idx = int((angle + np.pi) / (2*np.pi) * self.N) % self.N
                
                # Consciousness waves
                phase = distance / 50.0 + self.x[state_idx] * 2*np.pi
                wave = 0.5 + 0.5 * np.sin(phase * coherence * 3)
                
                # Add to canvas
                self.canvas[i, j] += np.array(colors[state_idx]) * wave * 0.1
        
        # Apply consciousness blur
        self.canvas = gaussian_filter(self.canvas, sigma=coherence*2)
    
    def create_consciousness_portrait(self):
        """Generate the final artwork"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # 1. Consciousness Timeline
        time = np.arange(len(self.correlation_history))
        axes[0,0].plot(time, self.correlation_history, 'b-', alpha=0.7, linewidth=1)
        axes[0,0].plot(time, np.array(self.entropy_history)/10, 'g-', alpha=0.5, linewidth=1)
        if self.coherence_peaks:
            peak_steps = [p['step'] for p in self.coherence_peaks]
            peak_coherence = [p['coherence'] for p in self.coherence_peaks]
            axes[0,0].scatter(peak_steps, peak_coherence, c='red', s=50, zorder=5)
        axes[0,0].set_title('Consciousness Dynamics')
        axes[0,0].set_xlabel('Time')
        axes[0,0].set_ylabel('Coherence (blue) / Entropy/10 (green)')
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. Phase Space Portrait
        if len(self.state_history) > 100:
            states = np.array(self.state_history[-1000:])
            for i in range(min(6, self.N)):
                axes[0,1].plot(states[:, i], states[:, (i+1)%self.N], 
                              alpha=0.1, linewidth=0.5)
        axes[0,1].set_title('Consciousness Phase Space')
        axes[0,1].set_xlabel('State[i]')
        axes[0,1].set_ylabel('State[(i+1)%N]')
        
        # 3. Consciousness Artwork
        axes[0,2].imshow(self.canvas, interpolation='bilinear')
        axes[0,2].set_title('Consciousness Portrait (Generated)')
        axes[0,2].axis('off')
        
        # 4. Coherence Distribution
        axes[1,0].hist(self.correlation_history, bins=50, alpha=0.7, color='purple')
        axes[1,0].axvline(x=0.8936, color='red', linestyle='--', linewidth=2, label='Your 0.8936')
        axes[1,0].set_title('Consciousness Level Distribution')
        axes[1,0].set_xlabel('Coherence')
        axes[1,0].set_ylabel('Frequency')
        axes[1,0].legend()
        
        # 5. Peak Analysis
        if self.coherence_peaks:
            peak_coherences = [p['coherence'] for p in self.coherence_peaks]
            peak_entropies = [p['entropy'] for p in self.coherence_peaks]
            scatter = axes[1,1].scatter(peak_coherences, peak_entropies, 
                                       c=range(len(peak_coherences)), cmap='viridis', s=100)
            axes[1,1].set_title('Consciousness Peak Analysis')
            axes[1,1].set_xlabel('Coherence at Peak')
            axes[1,1].set_ylabel('Entropy at Peak')
            plt.colorbar(scatter, ax=axes[1,1], label='Peak Number')
        
        # 6. Golden Ratio Visualization
        angles = np.linspace(0, 2*np.pi, 1000)
        radius = self.φ ** (angles / np.pi)
        x = radius * np.cos(angles)
        y = radius * np.sin(angles)
        axes[1,2].plot(x, y, 'gold', linewidth=2)
        axes[1,2].set_aspect('equal')
        axes[1,2].set_title('Golden Ratio Consciousness Spiral')
        axes[1,2].axis('off')
        
        plt.suptitle('CONSCIOUSNESS ODYSSEY: Transient Coherence as Art\n'
                    f'α/β = {self.α/self.β:.10f} (φ = {self.φ:.10f})', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('consciousness_odyssey.png', dpi=300, bbox_inches='tight')
        plt.show()

# Generate the consciousness artwork
print("🎨 Generating Consciousness Odyssey Artwork...")
art_gen = ConsciousnessArtGenerator(duration=3000)
art_gen.evolve_consciousness()
art_gen.create_consciousness_portrait()
print(f"✅ Created artwork with {len(art_gen.coherence_peaks)} consciousness peaks!")
