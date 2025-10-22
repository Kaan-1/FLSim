import numpy as np
import matplotlib.pyplot as plt
import os

def generate_linear_plot(real_slope, real_constant, starting_x, ending_x, error_var, slopes, constants, no_of_points, file_name):
    """
    Generate a plot with a real line and multiple groups of noisy points.
    
    Parameters:
    - real_slope: float, slope of the real line
    - real_constant: float, y-intercept of the real line
    - starting_x: float, minimum x value for the range
    - ending_x: float, maximum x value for the range
    - error_var: float, variance for the normal noise added to points
    - slopes: list of floats, slopes for each group
    - constants: list of floats, y-intercepts for each group (same size as slopes)
    """
    
    # Validate input
    if len(slopes) != len(constants):
        raise ValueError("slopes and constants lists must have the same length")
    
    # Create figure and axis
    plt.figure(figsize=(10, 8))
    
    # Generate x values for the real line (smooth curve)
    x_real = np.linspace(starting_x, ending_x, 1000)
    y_real = real_slope * x_real + real_constant
    
    # Plot the real line (in front, with higher zorder)
    plt.plot(x_real, y_real, 'k-', linewidth=3, label='Real Line', zorder=10)
    
    # Generate and plot points for each group
    colors = plt.cm.tab10(np.linspace(0, 1, len(slopes)))  # Generate distinct colors
    
    for i, (slope, constant, number_of_points) in enumerate(zip(slopes, constants, no_of_points)):
        # Generate 50 random x values between starting_x and ending_x
        x_points = np.random.uniform(starting_x, ending_x, number_of_points)
        
        # Calculate y values using the group's line equation
        y_base = slope * x_points + constant
        
        # Add normal noise with variance error_var
        noise = np.random.normal(0, np.sqrt(error_var), number_of_points)
        y_points = y_base + noise
        
        # Plot the points for this group
        plt.scatter(x_points, y_points, color=colors[i], alpha=0.7, 
                   s=30, label=f'Group {i+1}', zorder=5)
    
    # Customize the plot
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.title(file_name, fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    file_path = os.path.join("dataset_visualizations", f"{file_name}.png")
    plt.savefig(file_path)
    plt.close()

# Example usage
if __name__ == "__main__":
    # Example parameters
    real_slope = 2.0
    real_constant = 5.0
    starting_x = 0.0
    ending_x = 10.0
    
    # homo_low_dev
    generate_linear_plot(real_slope, real_constant, starting_x, ending_x, 
                        1, [2.0], [5.0], [150],
                        "homo_low_dev")
    
    # homo_high_dev
    generate_linear_plot(real_slope, real_constant, starting_x, ending_x, 
                        5, [2.0], [5.0], [150],
                        "homo_high_dev")
    
    # semi_homo_low_dev
    generate_linear_plot(real_slope, real_constant, starting_x, ending_x, 
                        1, [2.0, 2.0, 3.0, 2.0, 1.0], [5.0, 6.0, 5.0, 4.0, 5.0], [30, 30, 30, 30, 30],
                        "semi_homo_low_dev")
    
    # semi_homo_high_dev
    generate_linear_plot(real_slope, real_constant, starting_x, ending_x, 
                        5, [2.0, 2.0, 3.0, 2.0, 1.0], [5.0, 6.0, 5.0, 4.0, 5.0], [30, 30, 30, 30, 30],
                        "semi_homo_high_dev")
    
    # hetero_low_dev
    generate_linear_plot(real_slope, real_constant, starting_x, ending_x, 
                        1, [2.0, 2.0, 4.0], [5.0, 7.0, 5.0], [50, 50, 50],
                        "hetero_low_dev")
    
    # hetero_high_dev
    generate_linear_plot(real_slope, real_constant, starting_x, ending_x, 
                        5, [2.0, 2.0, 4.0], [5.0, 7.0, 5.0], [50, 50, 50],
                        "hetero_high_dev")