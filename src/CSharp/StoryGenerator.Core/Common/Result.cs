namespace StoryGenerator.Core;

/// <summary>
/// Represents the result of an operation that may succeed or fail.
/// </summary>
/// <typeparam name="T">Type of the success value.</typeparam>
public class Result<T>
{
    /// <summary>
    /// Gets a value indicating whether the operation succeeded.
    /// </summary>
    public bool IsSuccess { get; }

    /// <summary>
    /// Gets a value indicating whether the operation failed.
    /// </summary>
    public bool IsFailure => !IsSuccess;

    /// <summary>
    /// Gets the success value if the operation succeeded.
    /// </summary>
    public T? Value { get; }

    /// <summary>
    /// Gets the error message if the operation failed.
    /// </summary>
    public string? Error { get; }

    /// <summary>
    /// Gets the exception if the operation failed with an exception.
    /// </summary>
    public Exception? Exception { get; }

    private Result(bool isSuccess, T? value, string? error, Exception? exception)
    {
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
        Exception = exception;
    }

    /// <summary>
    /// Creates a successful result.
    /// </summary>
    /// <param name="value">The success value.</param>
    /// <returns>A successful result.</returns>
    public static Result<T> Success(T value)
    {
        return new Result<T>(true, value, null, null);
    }

    /// <summary>
    /// Creates a failed result with an error message.
    /// </summary>
    /// <param name="error">The error message.</param>
    /// <returns>A failed result.</returns>
    public static Result<T> Failure(string error)
    {
        return new Result<T>(false, default, error, null);
    }

    /// <summary>
    /// Creates a failed result with an exception.
    /// </summary>
    /// <param name="exception">The exception.</param>
    /// <returns>A failed result.</returns>
    public static Result<T> Failure(Exception exception)
    {
        return new Result<T>(false, default, exception.Message, exception);
    }

    /// <summary>
    /// Creates a failed result with an error message and exception.
    /// </summary>
    /// <param name="error">The error message.</param>
    /// <param name="exception">The exception.</param>
    /// <returns>A failed result.</returns>
    public static Result<T> Failure(string error, Exception exception)
    {
        return new Result<T>(false, default, error, exception);
    }

    /// <summary>
    /// Matches the result and executes the appropriate function.
    /// </summary>
    /// <typeparam name="TResult">The return type.</typeparam>
    /// <param name="success">Function to execute if successful.</param>
    /// <param name="failure">Function to execute if failed.</param>
    /// <returns>The result of the executed function.</returns>
    public TResult Match<TResult>(
        Func<T, TResult> success,
        Func<string, TResult> failure)
    {
        return IsSuccess ? success(Value!) : failure(Error ?? "Unknown error");
    }

    /// <summary>
    /// Maps the success value to a new type.
    /// </summary>
    /// <typeparam name="TNew">The new type.</typeparam>
    /// <param name="mapper">Function to map the value.</param>
    /// <returns>A new result with the mapped value.</returns>
    public Result<TNew> Map<TNew>(Func<T, TNew> mapper)
    {
        return IsSuccess
            ? Result<TNew>.Success(mapper(Value!))
            : Result<TNew>.Failure(Error ?? "Unknown error");
    }

    /// <summary>
    /// Binds the result to a new operation.
    /// </summary>
    /// <typeparam name="TNew">The new type.</typeparam>
    /// <param name="binder">Function to bind the result.</param>
    /// <returns>A new result from the bound operation.</returns>
    public Result<TNew> Bind<TNew>(Func<T, Result<TNew>> binder)
    {
        return IsSuccess
            ? binder(Value!)
            : Result<TNew>.Failure(Error ?? "Unknown error");
    }
}
