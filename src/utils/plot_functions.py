import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#---------------------------------------------------
#                 Plot Settings                    |
#---------------------------------------------------
plt.style.use("seaborn-v0_8-deep")
plt.rcParams["figure.figsize"] = [6, 4]
plt.rcParams["figure.dpi"] = 300



#---------------------------------------------------
#                 Save Any Figure                  |
#---------------------------------------------------
def save_fig(figure, save_path, fig_name, format='png'):
    try:
        os.makedirs(save_path, exist_ok=True)
        plot_save_path = os.path.join(save_path, f"{fig_name}.{format}")
        figure.savefig(plot_save_path, bbox_inches='tight', dpi=300)
        plt.show()
        plt.close(figure)
        print(f"Saved at {plot_save_path}")
    except (FileNotFoundError, OSError) as e:
        print(f"Error saving figure: {e}")


#---------------------------------------------------
#         Box Plots Continuous Features            |
#---------------------------------------------------
def grouped_boxplots(data_frame):
    # Filter out continuous features with cardinality > 9
    continuous_features = data_frame.select_dtypes(include='number')
    selected_features = continuous_features.columns[continuous_features.nunique() > 9]

    # Calculate the number of rows and columns for the subplots
    num_plots = len(selected_features)
    num_cols = min(num_plots, 2)
    num_rows = (num_plots + 1) // 2

    # Create subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 4 * num_rows))
    fig.subplots_adjust(hspace=0.5)

    if num_plots == 1:
        axes = [axes]

    for i, feature in enumerate(selected_features):
        ax = axes[i // num_cols][i % num_cols]
        ax.boxplot(data_frame[feature].dropna(), vert=True, showmeans=True, meanline=True, patch_artist=True)
        ax.set_title(feature)

        # Calculate mean, median, min and max values
        mean_value = data_frame[feature].mean()
        median_value = data_frame[feature].median()
        min_value = data_frame[feature].min()
        max_value = data_frame[feature].max()

        # Add mean, median, min, and max labels 
        x_coord = 1.2  
        y_coord_mean = mean_value + 0.3
        y_coord_median = median_value + 0.3
        y_coord_min = min_value + 0.51
        y_coord_max = max_value - 0.5
        ax.text(x_coord, y_coord_mean, f'Mean: {mean_value:.2f}', va='top', ha='left', fontweight='bold')
        ax.text(x_coord, y_coord_median, f'Median: {median_value:.2f}', va='bottom', ha='left', fontweight='bold')
        ax.text(x_coord, y_coord_min, f'Min: {min_value:.2f}', va='bottom', ha='left', fontweight='bold')
        ax.text(x_coord, y_coord_max, f'Max: {max_value:.2f}', va='top', ha='left', fontweight='bold')

    # Remove extra axes if there are any empty subplots
    for i in range(len(selected_features), num_rows * num_cols):
        fig.delaxes(axes[i // num_cols][i % num_cols])

    # Padding
    fig.tight_layout(pad=3.0)
    
    return fig  # Return the figure object for saving

def save_grouped_boxplot(fig, save_path=None):
    # Save the combined plot
    if save_path:
        os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
        combined_plot_save_path = os.path.join(save_path, "grouped_boxplots.png")
        fig.savefig(combined_plot_save_path, bbox_inches='tight', dpi=300)
        plt.close(fig)  # Close the figure after saving to prevent display issues
    
    print(f"Saved at {combined_plot_save_path}")
    
    
#---------------------------------------------------
#          Histograms Continuous Features          |
#---------------------------------------------------
def grouped_histograms(dataframe):
    # Get the list of column names with continuous features
    continuous_cols = dataframe.select_dtypes(include=['float64', 'int64']).columns

    # Filter columns with cardinality > 10
    selected_cols = [col for col in continuous_cols if dataframe[col].nunique() > 10]

    # Calculate the number of rows and columns for the subplots
    n_rows = len(selected_cols) // 2 + len(selected_cols) % 2
    n_cols = min(2, len(selected_cols))

    # Create subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 4 * n_rows))
    fig.tight_layout(pad=3.0)

    # Plot histograms for each selected column
    for i, col in enumerate(selected_cols):
        row_index = i // n_cols
        col_index = i % n_cols
        if n_rows > 1:
            ax = axes[row_index, col_index]
        else:
            ax = axes[col_index]
        dataframe[col].plot.hist(ax=ax, bins=25, edgecolor='black')
        ax.set_title(col)

    # Remove any empty subplots
    if len(selected_cols) < n_rows * n_cols:
        for i in range(len(selected_cols), n_rows * n_cols):
            fig.delaxes(axes.flatten()[i])

    # Using padding
    fig.tight_layout(pad=3.0)
    
    return fig


def save_grouped_histograms(fig, save_path=None):
    # Save the combined histogram plot
    if save_path:
        os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
        combined_hist_plot_save_path = os.path.join(save_path, "grouped_histograms.png")
        fig.savefig(combined_hist_plot_save_path, bbox_inches='tight', dpi=300)
        plt.close(fig)  # Close the figure after saving to prevent display issues
        
    print(f"Saved at {save_path}")



#---------------------------------------------------------
#     Single Stacked Bar Plot Categorical Features       |
#---------------------------------------------------------
def stacked_plot(df, feature, save_path=None):
    # Create a DataFrame containing value counts of the specified feature
    # Reset the index to have the categories as a regular column
    # Rename the 'count' column to match the specified feature name
    df = pd.DataFrame(df[feature].value_counts()).reset_index().rename({'count': feature})

   # Calculate the total count for the specified feature
    try:
        # Find the index of the specified feature
        feature_index = df.columns.get_loc(feature)
        
        # Check if the feature is not the last column
        if feature_index < len(df.columns) - 1:
            next_column_name = df.columns[feature_index + 1]
            total_count = float(df[next_column_name].sum())

            # Create a pivot table from the DataFrame
            # The pivot table will have the specified feature as columns and counts as values
            # The aggregation function used is 'sum' to aggregate counts for each category
            plt.figure(figsize=(6,4))
            
            pivot_table = pd.pivot_table(df, values='count',
                                        columns=[feature],
                                        aggfunc="sum").rename_axis(feature).reset_index()
            
            # Plot a stacked bar chart using the pivot table
            # The x-axis is set to the specified feature
            # The bars will be stacked, so each category contributes to the total
            ax = pivot_table.plot(figsize=(6,4), colormap='viridis', x=feature, kind='bar', stacked=True)
           
            # Customize the x-axis label and make it larger
            plt.xlabel(feature, fontsize=8)

            # Hide the x-axis ticks to make the chart cleaner
            plt.xticks(visible=False)
            
            # Display the count values as percentages on top of the bars
            for p in ax.patches:
                width, height = p.get_width(), p.get_height()
                x, y = p.get_xy()
                percentage = (height / total_count) * 100  # Calculate percentage
                ax.annotate(f'{percentage:.1f}%', (x + width / 2, y + height), ha='center')
                
            
             # Save the chart if save_path is provided
            if save_path:
                os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
                stacked_barplot_save_path = os.path.join(save_path, "{}_stacked_barplot.png".format(feature))
                plt.savefig(stacked_barplot_save_path, bbox_inches='tight', dpi=300)
                
                # Show the chart
                plt.show()
                plt.close()
                print(f"Saved at {save_path}") 
            
               
        else:
            raise ValueError("The specified feature is the last column in the DataFrame.")
    except KeyError:
        raise ValueError(f"Feature '{feature}' not found in the DataFrame.")
    
    
    
#---------------------------------------------------------
#     Get Stacked Bar Plots Categorical Features         |
#---------------------------------------------------------    
def grouped_stacked_bars(dataframe, save_path=None):
    # Select columns with categorical features (low cardinality)
    categorical_cols = [col for col in dataframe.columns if dataframe[col].nunique() < 10]
    
    # Determine the number of rows and columns for the subplots grid
    n_rows = len(categorical_cols) // 2 + len(categorical_cols) % 2
    n_cols = min(2, len(categorical_cols))

    # Create subplots grid
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 4 * n_rows))
    fig.tight_layout(pad=3.0)

    # Iterate over each categorical column to plot its stacked bar chart
    for i, col in enumerate(categorical_cols):
        # Set the correct axis for the subplot
        row_index = i // n_cols
        col_index = i % n_cols
        ax = axes[row_index, col_index] if n_rows > 1 else axes[col_index]

        # Prepare the data for stacked bar plotting
        value_counts = dataframe[col].value_counts(normalize=True).sort_index()  # Normalize to get percentages

        # Generate a color gradient based on the values
        colors = [plt.cm.YlOrRd(value) for value in value_counts]  

        # Plot with gradient colors
        value_counts.plot(kind='bar', stacked=True, ax=ax, color=colors, edgecolor='black')
        
        # Customize the plot appearance
        ax.set_title(col)
        ax.set_xlabel('')
        ax.set_ylabel('Proportion')
        
        # Display percentage annotations on each bar
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height * 100:.1f}%', (p.get_x() + p.get_width() / 2, height), 
                        ha='center', va='bottom')

    # Remove any empty subplots if there are fewer features than subplots
    if len(categorical_cols) < n_rows * n_cols:
        for j in range(len(categorical_cols), n_rows * n_cols):
            fig.delaxes(axes.flatten()[j])

    # Save the entire figure if a path is provided
    if save_path:
            os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
            combined_hist_plot_save_path = os.path.join(save_path, "grouped_stacked_barplot.png")
            plt.savefig(combined_hist_plot_save_path, bbox_inches='tight', dpi=300)
            plt.close(fig)
            print(f"Saved at {save_path}") 
    else:
        plt.show()
    
    plt.close(fig)  # Close the figure to free memory and prevent display issues
        
    

#---------------------------------------------------------
#             Get Bar Plots of Null Values               |
#---------------------------------------------------------    
def total_nulls_barplot(df):
    # Calculate the number of null and non-null values for each column
    total_counts = len(df)
    null_counts = df.isnull().sum()
    non_null_counts = df.notnull().sum()

    # Calculate null and non-null percentages
    null_percentages = (null_counts / total_counts) * 100
    non_null_percentages = (non_null_counts / total_counts) * 100

    # Create a bar plot to visualize null and non-null percentages
    fig, ax = plt.subplots(figsize=(6, 4))  # Use subplots to manage fig and ax objects
    ax.bar(non_null_counts.index, non_null_percentages, bottom=null_percentages, color='blue', alpha=0.7, label='Non-null')
    ax.bar(null_counts.index, null_percentages, color='red', alpha=0.7, label='Null')
    ax.set_title('Null vs Non-null Value Percentages by Column')
    ax.set_xlabel('Columns')
    ax.set_ylabel('Percentage')
    ax.set_xticklabels(non_null_counts.index, rotation=90)
    ax.legend()

    # Display the percentages as labels on top of the bars
    for i, (null_percentage, non_null_percentage) in enumerate(zip(null_percentages, non_null_percentages)):
        ax.text(i, null_percentage + non_null_percentage / 2, f'{null_percentage:.1f}%', ha='center', va='top')

    return fig  # Return the figure object for saving

def save_total_nulls_barplot(fig, save_path=None):    
    # Save the bar plot
    if save_path:
        os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
        combined_plot_save_path = os.path.join(save_path, "total_nulls_barplot.png")
        fig.savefig(combined_plot_save_path, bbox_inches='tight', dpi=300)
        plt.close(fig)  # Close the figure after saving to prevent display issues
    
    print(f"Saved at {combined_plot_save_path}")  
            
        
        
#-------------------------------------------------------------------
#             BIVARIATE ANALYSIS CLASSIFICATION TASK               |
#-------------------------------------------------------------------
#               GROUPED HISTOGRAMS vs TARGET LABEL                 |
#-------------------------------------------------------------------       
def biv_grouped_histograms(data_frame, target):
    # Filter out continuous variables based on cardinality
    continuous_cols = data_frame.select_dtypes(include=['float64', 'int64']).columns

    # Filter columns with cardinality > 10
    selected_cols = [col for col in continuous_cols if data_frame[col].nunique() > 10]
    
    # Set the number of bins for the histograms
    num_bins = 25
    
    # Create subplots
    num_plots = len(selected_cols)
    num_cols = min(num_plots, 2)
    num_rows = (num_plots + 1) // 2

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 4 * num_rows))
    fig.tight_layout(pad=3.0)

    # Plot grouped histograms
    for i, col in enumerate(selected_cols):
        row_index = i // num_cols
        col_index = i % num_cols
        if num_rows > 1:
            ax = axes[row_index, col_index]
        else:
            ax = axes[col_index]
        
        # Create histograms for each unique value of the target variable
        for target_value in data_frame[target].unique():
            sns.histplot(data_frame[data_frame[target] == target_value], x=col, ax=ax, bins=num_bins, label=f'{target}={target_value}', common_norm=False)

        ax.set_title(col)
        ax.legend()
    
    # Remove any empty subplots
    if num_plots < num_rows * num_cols:
        for i in range(num_plots, num_rows * num_cols):
            fig.delaxes(axes.flatten()[i])

    return plt

def save_biv_grouped_histograms(plot, save_path=None):
    # Save the chart if save_path is provided
    if save_path:
        os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
        grouped_hist_save_path = os.path.join(save_path, "grouped_histograms_vs_target.png")
        plot.savefig(grouped_hist_save_path, bbox_inches='tight', dpi=300)
        print(f"Saved at {grouped_hist_save_path}")
        plt.show()


#-------------------------------------------------------------------
#                GROUPED BOX PLOTS vs TARGET LABEL                 |
#-------------------------------------------------------------------
def biv_grouped_boxplots(data_frame, target, save_path=None):
    # Filter out continuous variables based on cardinality
    continuous_cols = data_frame.select_dtypes(include=['float64', 'int64']).columns

    # Filter columns with cardinality > 10
    selected_cols = [col for col in continuous_cols if data_frame[col].nunique() > 10]
    
    # Filter out the target variable from selected_cols
    selected_cols = [col for col in selected_cols if col != target]
    
    if save_path:
        os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
                
    # List to store the generated plot filenames
    generated_plots = []

    # Create a grouped boxplot for each continuous feature and save it
    for col in selected_cols:
        plt.figure(figsize=(8, 4))
        sns.boxplot(data=data_frame, x=target, y=col)
        
        # Set plot title and labels
        plt.title(f'{col} vs {target}')
        plt.xlabel(target)
        plt.ylabel(col)
        
        if save_path:
            # Create the directory if it doesn't exist 
            os.makedirs(save_path, exist_ok=True)     
            
            # Save the plot with an appropriate filename
            plot_filename = os.path.join(save_path, f'{col}_vs_{target}_boxplot.png')
            plt.savefig(plot_filename)
            generated_plots.append(plot_filename)
            
            # Close the current plot
            plt.close()  
        
    # Return the list of generated plot filenames
    return generated_plots
        
        
#-------------------------------------------------------------------
#                GROUPED BAR PLOTS vs TARGET LABEL                 |
#-------------------------------------------------------------------
def biv_grouped_barplots(data_frame, target, save_path=None):
    # Filter out categorical variables based on cardinality
    categorical_cols = data_frame.select_dtypes(include=['object']).columns

    # Filter columns with cardinality < 9
    selected_cols = [col for col in categorical_cols if data_frame[col].nunique() < 9]

    filtered_df = data_frame[selected_cols + [target]]

    # List to store the generated plot filenames
    generated_plots = []

    for col in filtered_df.columns:
        # Skip plotting when col is equal to the target variable
        if col == target:
            continue

        # Plot size
        plt.figure(figsize=(8, 4))

        # Bar plots
        sns.countplot(data=filtered_df, x=col, hue=target)

        # Set plot title and labels
        plt.title(f'{col}')
        plt.xlabel(col)
        plt.ylabel('Count')

        # Save the plot with an appropriate filename
        if save_path:
            # Create the directory if it doesn't exist 
            os.makedirs(save_path, exist_ok=True) 
            plot_filename = os.path.join(save_path, f'{col}_vs_{target}barplot.png')
            plt.savefig(plot_filename)
            generated_plots.append(plot_filename)
            
            # Close the current plot
            plt.close()  

    # Return the list of generated plot filenames
    return generated_plots


        
#-------------------------------------------------------------------
#                        CORRELATION HEATMAP                       |
#-------------------------------------------------------------------
def plot_correlation_heatmap(data_frame):
    # Label 'object' type categorical features
    categorical_cols = data_frame.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        data_frame[col] = data_frame[col].astype('category').cat.codes

    # Calculate the correlation matrix
    correlation_matrix = data_frame.corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(12, 10))

    # Create a heatmap using seaborn
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")

    # Set plot title
    plt.title('Correlation Heatmap')

    # Show the plot
    return plt

def save_corr_heatmap(plot, save_path=None):
    # Save the chart if save_path is provided
    if save_path:
        os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
        individual_boxplot_save_path = os.path.join(save_path, f"Corr_heatmap.png")
        plot.savefig(individual_boxplot_save_path, bbox_inches='tight', dpi=300)
    
        print(f"Saved at {save_path}")
        
        

#-------------------------------------------------------------------
#                        CORRELATION PAIRPLOT                      |
#-------------------------------------------------------------------
def plot_pairplot(df, target, save_path=None):
    plt.figure(figsize=(20,20))
    sns.pairplot(df.sample(1000), hue=target)

    if save_path:
        # Create the directory if it doesn't exist 
        os.makedirs(save_path, exist_ok=True)     
        plot_filename = os.path.join(save_path, f'Pairplot_vs_{target}.png')
        plt.savefig(plot_filename)
                
        # Close the current plot
        plt.close() 
        
        
        
        
        
#---------------------------------------------------------------------------
#                        PLOT SCORES with H BAR PLOT                       |
#---------------------------------------------------------------------------
def plot_scores(algorithms, scores, title, save_path=None):
    # Create a bar chart
    plt.figure(figsize=(8, 6))
    plt.barh(algorithms, scores, color='skyblue')
    plt.xlabel('Score')
    plt.ylabel('Algorithms')
    plt.title(f'{title}')
    plt.xlim(0, 1)  # Set the x-axis limits between 0 and 1 (assuming accuracy is in [0, 1])

    # Display the accuracy scores on the bars
    for i, score in enumerate(scores):
        plt.text(score + 0.02, i, f'{score:.2f}', va='center')

    plt.tight_layout()

    if save_path:
        # Create the directory if it doesn't exist 
        os.makedirs(save_path, exist_ok=True)     
        plot_filename = os.path.join(save_path, f'{title}.png')
        plt.savefig(plot_filename)
            
    return plt





#---------------------------------------------------------------------------
#                   PLOT PRECISION-RECALL CURVE PLOT                       |
#---------------------------------------------------------------------------
def plot_precision_recall_curve(y_true, y_scores, save_path=None):
    precision, recall, thresholds = precision_recall_curve(y_true, y_scores)

    # Calculate Precision-Recall AUC
    pr_auc = auc(recall, precision)

    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color='b', lw=2, label=f'Precision-Recall AUC = {pr_auc:.3f}')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall Curve')
    plt.grid()
    plt.legend(loc='lower left')
    
    # Save figure
    if save_path:
        os.makedirs(save_path, exist_ok=True)
        precision_recall_curve_save_path = os.path.join(save_path, "precision_recall_curve.png")
        plt.savefig(precision_recall_curve_save_path, bbox_inches='tight', dpi=300)
    print(f"Saved at {save_path}")

    return plt


#---------------------------------------------------------------------------
#                        PLOT ROC AUC CURVE PLOT                           |
#---------------------------------------------------------------------------
def plot_roc_auc_curve(y_true, y_scores, save_path=None):
    # ROC AUC Curve
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)

    # Calculate ROC AUC
    roc_auc = roc_auc_score(y_true, y_scores)

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = {:.3f})'.format(roc_auc))
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc='lower right')
    
    # Save the plot
    if save_path:
        # Create the directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)  
        roc_auc_curve_save_path = os.path.join(save_path, "roc_auc_curve.png")
        plt.savefig(roc_auc_curve_save_path, bbox_inches='tight', dpi=300)
    print(f"Saved at {save_path}")
    
    return plt



#---------------------------------------------------------------------------
#                  PLOT FEATURE IMPORTANCES BAR PLOTS                      |
#---------------------------------------------------------------------------
def plot_feature_importances(clf_feature_importance, feature_names, save_path=None):
    # Name of the classifier
    clf_name = clf_feature_importance.__class__.__name__
    
    # Create a DataFrame to store feature names and importances
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': clf_feature_importance})

    # Sort the DataFrame by importance in descending order
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

    # Create a bar plot to visualize feature importances
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title(f'Feature Importance for Churn Prediction - {clf_name}')
    plt.gca().invert_yaxis()  # Invert the y-axis for better readability
    
    # Save plot
    if save_path:
        os.makedirs(save_path, exist_ok=True)
        feature_importance_plot_save_path = os.path.join(save_path, "feature_importance.png")
        plt.savefig(feature_importance_plot_save_path, bbox_inches="tight", dpi=300)
    print(f"Saved at {save_path}")

    return plt