kp_val = [1, 2, 4, 8, 16, 20];
%kp_val = [2, 20];
figure;
hold on;

for i = 1:length(kp_val)
    kp = kp_val(i);
    filename = sprintf("straight_data/control_data_kp%d.csv", kp);
    data = readtable(filename);
    
    % Time Splice
    idx = data.time >= 210;

    % Noise/Smoothing Filter
    heading = data.current_response;
    smooth_heading = movmean(heading, 5);

    plot(data.time(idx), smooth_heading(idx), 'LineWidth', 1.5, ...
        'DisplayName', sprintf("Kp = %d", kp));
end

% Baseline
data0 = readtable("straight_data/control_data_base.csv");
plot(data0.time(idx), data0.current_response(idx), 'LineWidth', 1.5, ...
    'DisplayName', "Baseline");

yline(0, '--', 'LineWidth', 1, 'DisplayName', "Target");

xlabel("Time (ms)");
ylabel("Heading (degrees)");
title("Heading Response for Different Kp Values (Straight)");
legend("show")
grid on;
hold off;